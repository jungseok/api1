from flask import Flask, jsonify, request, Response, g
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import ast
import json
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is secr3311et'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warranty_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# # # # # # # # # # # # # # # #  Entity Model Start  # # # # # # # # # # # # # # # #
class Institution(db.Model):
    __tablename__ = "institution"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    institute_code = db.Column(db.Text, primary_key=True)
    institute_name = db.Column(db.Text)
    year = db.Column(db.Text)
    month = db.Column(db.Text)
    amount = db.Column(db.Text)

    def __init__(self, id, name, year, month, amount):
        self.institute_code = id
        self.institute_name = name
        self.year = year
        self.month = month
        self.amount = amount

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    user_id = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text)
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

# # # # # # # # # # # # # # # #  Entity Model End  # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #  JWT Add Start  # # # # # # # # # # # # # # # #

from datetime import datetime, timedelta
import jwt
from functools import wraps
import bcrypt

JWT_SECRET = 'this is se3c345ret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 1800

@app.route('/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    enc_p = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    user = User( username, enc_p )

    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return Response(error, status=401)

    #if username != 'test' or password != 'test':
    #    return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    payload = {
        'user_id': username,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    print(payload)

    jwt_token = jwt.encode(payload, JWT_SECRET, 'HS256')
    print(JWT_SECRET)
    return jsonify({'token': jwt_token.decode('utf-8')})


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    u = db.session.query(User).filter_by(user_id=username)
    if u is None:
        return Response("user not found", status=401)
    else:
        for uu in u:
            print(password.encode("UTF-8"))
            print(uu.password)
            if not bcrypt.checkpw(password.encode("UTF-8"), uu.password):
                return Response("incorrect password", status=401)

    #if username != 'test' or password != 'test':
    #    return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    payload = {
        'user_id': username,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    print(payload)

    jwt_token = jwt.encode(payload, JWT_SECRET, 'HS256')
    print(JWT_SECRET)
    return jsonify({'token': jwt_token.decode('utf-8')})


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization", None)
        print(access_token)
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, JWT_SECRET, algorithms=['HS256'])
                print(JWT_SECRET)
                print(payload)
            except jwt.InvalidTokenError:
                print("error")
                payload = None

            if payload is None:
                return Response(status=401)

            user_id = payload["user_id"]
            g.user_id = user_id
            #g.user = get_user_info(user_id) if user_id else None
            g.user = "ttt" if user_id else None
        else:
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated_function

@app.route('/refresh_token', methods=['POST'])
def refresh_token():
    access_token = request.headers.get("Authorization", None)
    print(access_token)
    if access_token is not None:
        try:
            if access_token.startswith("Bearer "):
                access_token = access_token.split(" ")[1]

            print(access_token)
            payload = jwt.decode(access_token, JWT_SECRET, algorithms=['HS256'])
            print(JWT_SECRET)
            print(payload)
        except jwt.InvalidTokenError:
            print("error")
            payload = None

        if payload is None:
            return Response(status=401)

        # Identity can be any data that is json serializable
        payload['exp'] = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        print(payload)

        jwt_token = jwt.encode(payload, JWT_SECRET, 'HS256')
        print(JWT_SECRET)
    else:
        return Response(status=401)

    return jsonify({'token': jwt_token.decode('utf-8')})


@app.route('/protected', methods=['POST'])
@login_required
def protected2():
    print("d")
    return jsonify({"allowed to": g.user_id}), 200

# # # # # # # # # # # # # # # #  JWT Add End  # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #  API Logic Start  # # # # # # # # # # # # # # # #
def get_dataframe():

    df = None

    for i in Institution.query.all():
        name = i.institute_name
        year = ast.literal_eval(i.year)
        month = ast.literal_eval(i.month)
        amount = list(map(lambda x: int(x.replace(",","")) if type(x) == str else x, ast.literal_eval(i.amount)))

        df2 = pd.DataFrame(amount, columns=[name])
        if df is None:
            dfy = pd.DataFrame(year, columns=["year"])
            dfm = pd.DataFrame(month, columns=["month"])
            df = dfy
            df = df.join(dfm)
            df = df.join(df2)
        else:
            df = df.join(df2)

    return df

def predict_amt(req_bankname, req_month):
    from pandas import Series
    from matplotlib import pyplot
    #pd.pivot_table(df.loc[df['year'] != 2006], values="농협은행/수협은행",
    #               columns="year", index="month").plot(subplots=True, figsize=(12, 12), layout=(3, 5), sharey=True);

    #pyplot.show()

    print(req_bankname)
    df = get_dataframe()

    ret = {}
    idx = 0
    for i, n in enumerate(df.columns):
        if n == req_bankname:
            idx = i

    dfy = df.loc[df['year'] == 2017]
    yearavg = list(map(float, (dfy.mean(skipna=True).values[2:])))

    code = ''
    for r in db.session.query(Institution).filter_by(institute_name=req_bankname):
        code = r.institute_code

    ret["bank"] = code
    ret["year"] = 2018
    ret["month"] = req_month
    ret["amount"] = int(yearavg[idx-2])

    return json.dumps(ret, ensure_ascii=False)


def foreign_avg():
    df = get_dataframe()

    ret = {}
    idx = 0
    for i, n in enumerate(df.columns):
        if n == '외환은행':
            idx = i

    al = []
    aly = []
    for y in df.year.unique():
        # print(y)
        dfy = df.loc[df['year'] == y]
        yearavg = list(map(float, (dfy.mean(skipna=True).values[2:])))

        al.append(round(yearavg[idx-2]))
        aly.append(y)

    al = al[:-1]
    aly = aly[:-1]

    support_amt = []

    ret['bank'] = "외환은행"
    elem = dict()
    elem['year'] = str(aly[al.index(min(al))])
    elem['amount'] = int(min(al))
    support_amt.append(elem)

    elem = dict()
    elem['year'] = str(aly[al.index(max(al))])
    elem['amount'] = int(max(al))
    support_amt.append(elem)

    ret["support_amount"] = support_amt

    return json.dumps(ret, ensure_ascii=False)


def max_institute():
    df = get_dataframe()

    ret = {}

    max_val = 0
    max_y = 0
    max_i = 0

    for y in df.year.unique():
        dfy = df.loc[df['year'] == y]
        yearsum = dfy.sum(skipna=True).values[2:]

        for i, d in enumerate(dfy.columns[2:]):
            if int(yearsum[i]) > max_val:
                max_val = int(yearsum[i])
                max_y = y
                max_i = i

    ret['year'] = int(max_y)
    ret['bank'] = df.columns[2:][max_i]

    return json.dumps(ret, ensure_ascii = False)


def annual_total_summary():
    df = get_dataframe()

    ret = {}
    year_list = []

    for y in df.year.unique():
        yr = {}

        dfy = df.loc[df['year'] == y]
        yr["year"] = str(y) + "년"

        yearsum = dfy.sum(skipna=True).values[2:]
        yr["total_amount"] = int(sum(yearsum))

        detail = {}
        for i, d in enumerate(dfy.columns[2:]):
            detail[d] = int(yearsum[i])

        yr["detail_amount"] = detail

        year_list.append(yr)

    ret['list'] = year_list
    return json.dumps(ret, ensure_ascii = False)


def read_institutions():
    idic = {}
    for i in Institution.query.all():
        idic [i.institute_code] = i.institute_name

    return json.dumps(idic, ensure_ascii = False)


def read_csv_file(filename):
    filename=str(filename).replace("'","")
    filename=filename.replace('"', "")
    filename = './' + filename

    import codecs
    data = codecs.open(filename, encoding='euc-kr')

    import pandas as pd
    df = pd.read_csv(data)
    # print(df.head())

    # iterating the columns
    code = 'inst'
    no = 0

    db.session.query(Institution).delete()

    for col in df.columns:
        if col[:7] != "Unnamed" and '(억원)' in col:
            no += 1
            ins = Institution(
                code + '%03d' % no,  # id
                col.replace("(억원)",""),  # name
                str(df['연도'].tolist()),  # year
                str(df['월'].tolist()),  # month
                str(df[col].tolist())  # amount
            )
            db.session.add(ins)
            db.session.commit()

    return json.dumps({ "read_instruments": no }, ensure_ascii = False)

# # # # # # # # # # # # # # # #  API Logic End  # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #  API Routing Start  # # # # # # # # # # # # # # # #

# 데이터 파일에서 각 레코드를 데이터베이스에 저장하는 API 개발
@app.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            content = request.json
            return read_csv_file(content['filename'])
        except Exception as e:
            return Response(status=401)

#주택금융 공급 금융기관(은행) 목록을 출력하는 API 를 개발하세요.
@app.route('/lists', methods=['POST'])
@login_required
def lists():
    if request.method == 'POST':
        try:
            return read_institutions()
        except Exception as e:
            return Response(status=401)

#년도별 각 금융기관의 지원금액 합계를 출력하는 API 를 개발하세요.
@app.route('/annual_total', methods=['POST'])
@login_required
def annual_total():
    if request.method == 'POST':
        try:
            return annual_total_summary()
        except Exception as e:
            return Response(status=401)

# 각 년도별 각 기관의 전체지원금액 중에서 가장 큰 금액의 기관명을 출력하는 API개발
@app.route('/max_inst', methods=['POST'])
@login_required
def max_inst():
    if request.method == 'POST':
        try:
            return max_institute()
        except Exception as e:
            return Response(status=401)

#전체 년도(2005~2016)에서 외환은행의 지원금액 평균 중에서 가장 작은 금액과 큰 금액을 출력하는 API 개발
@app.route('/foreign', methods=['POST'])
@login_required
def foreign():
    if request.method == 'POST':
        try:
            return foreign_avg()
        except Exception as e:
            return Response(status=401)

# 특정 은행의 특정 달에 대해서 2018년도 해당 달에 금융지원 금액을 예측하는 API 개발
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    print("d")
    if request.method == 'POST':
        try:
            print(request.json)
            content = request.json
            print(content)
            return predict_amt(content['bank'], content['month'])
        except Exception as e:
            return Response(status=401)

# # # # # # # # # # # # # # # #  API Routing End  # # # # # # # # # # # # # # # #

if __name__ == '__main__':

    # db table creation
    TABLE_CREATION_REQUIRED = 1
    if TABLE_CREATION_REQUIRED:
        db.create_all()

    RUN_SERVER = 1
    if RUN_SERVER:
        app.run(debug=True)
    else:
        #read_csv_file('서버개발_사전과제3_주택금융신용보증_금융기관별_공급현황.csv')
        #read_institutions()
        print(predict("우리은행", 2))