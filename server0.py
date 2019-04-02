from flask import Flask,g, render_template,request, redirect, url_for, session
from sqlalchemy import desc,or_,and_
import backend_alchemy
import sqlalchemy
import logging
import json
from  myutil import MyEncoder
from obj_sqlalchemy import *
import sys
import traceback
import datetime
import os, os.path, json, shutil
# app_root=os.path.normpath(mysite.settings.MEDIA_ROOT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app_root=os.path.normpath(BASE_DIR+os.path.sep+"static")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
def getdb():
    if "db" in g:
        pass
    else:
        g.db=backend_alchemy.Session()
    return g.db
# @app.route('/static/react1/build/index.html')
# def index():
#     return redirect(url_for('Contact'))
# socketio = SocketIO(app)
# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return 'Subpath %s' % subpath、
def file_url(path,file):
    logging.info(path)
    url="/static/"+path+file
    logging.info(url)
    return url
def true_path(path,file):
    logging.info(path)
    true=app_root+"/"+path
    if file!=None:
        true+=file
    logging.info(true)
    return true

@app.route("/explore/")
def explore():
    path=request.args.get("path")
    file=request.args.get("file")
    if path==None:
        path=""
    filepath=true_path(path,file)
    if os.path.isfile(filepath):
        r=redirect(file_url(path,file))
        return(r)
    if file!=None:
        path=path+file+"/"
    files=os.listdir(true_path(path,None))
    # output={"path":path,"files":files}
    #return HttpResponse(json.dumps(output, ensure_ascii=False))
    r=render_template("explore/index.html",path=path,files=files)
    return r
@app.route('/extjs/angular/')
def angular():
    # c={"user":request.user,"csrf_token":csrf(request)["csrf_token"]}
    r=render_template("extjs/angular.html")
    return(r)
        # url(r'^api/contacts$',views.contacts),
        # url(r'^api/contacts/(?P<id>\d+)$', views.contactOne),
@app.route("/extjs/api/contacts")    
def contacts():
    if request.method == 'GET':
        db=getdb()
        rec=db.query(PartsItem).all()
        output=[]
        for one in rec:
            output.append(one.json())
        return json.dumps(output, ensure_ascii=False)
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        contact=PartsItem.mycreate(data)
        contact.save()
        output=contact.json()
        return json.dumps(output, ensure_ascii=False)
@app.route("/extjs/api/contacts/<int:id>")            
def contactOne(id=None):
    if request.method == 'GET':
        rec=Item.objects.get(id=int(id))
        output=rec.json()
        return HttpResponse(json.dumps(output, ensure_ascii=False)) 
    if request.method == 'PUT':
        data = json.loads(request.body.decode("utf-8"))
        id=data.get("id")
        rec=Item.objects.get(id=int(id))
        rec.myupdate(data)
        rec.save()
        output=rec.json()
        return HttpResponse(json.dumps(output, ensure_ascii=False))         

@app.route('/extjs/react/')
def react():
    r=render_template("extjs/react.html")
    return(r)
@app.route('/parts/month12/')
def month12():
    logging.info("chart")
    db=getdb()
    # r=Contact.objects
    # .annotate(month=TruncMonth('tiaoshi_date'))  # Truncate to month and add to select list
    # .values('month')                          # Group By month
    # .annotate(c=Count('id'))                  # Select the count of the grouping
    # .values('month', 'c')  
    # logging.info(r)
    # logging.info(dir(r))
    end_date=datetime.datetime.now()
    #start_date=end_date+datetime.timedelta(-365)
    start_date=datetime.datetime(end_date.year-1,1,1,0,0,0)
    # query = Contact.objects.filter(tiaoshi_date__range=(start_date, end_date)).extra(select={'year': "EXTRACT(year FROM tiaoshi_date)",
    #                                           'month': "EXTRACT(month from tiaoshi_date)",
    #                                           'day': "EXTRACT(day from tiaoshi_date)"}

    #                                   ).values('year', 'month', 'day').annotate(Count('id'))
    # contacts=query.all()
    #Contact.objects.raw("select * from ");
    # cursor = connection.cursor()            #获得一个游标(cursor)对象
    #更新操作
    start_date_s=start_date.strftime("%Y-%m-%d")
    end_date_s=end_date.strftime("%Y-%m-%d")
    cmd="select strftime('%Y-%m',tiaoshi_date) as month,count(id) from parts_contact  where tiaoshi_date between '"+start_date_s+"' and '"+end_date_s+"' group by month"
    logging.info(cmd)
    cursor=db.execute(cmd)    #执行sql语句
    #transaction.commit_unless_managed()     #提交到数据库
    #查询操作
    #cursor.execute('select * from other_other2 where id>%s' ,[1])

    raw = cursor.fetchall()                 #返回结果行 或使用 #raw = cursor.fetchall()
    lbls=[]
    values=[]
    for one in raw:
        lbls.append(one[0]+"月")
        values.append(one[1])
    #如果连接多个数据库则使用django.db.connections
    #from django.db import connections
    #_cursor = connections['other_database'].cursor()
    #如果执行了更新、删除等操作
    #transaction.commit_unless_managed(using='other_databases')
    r=render_template("parts/chart.html",user="",lbls=lbls,values=values)
    return(r)

@app.route('/parts/items/')
def items():
        #         第{{ page.number }}页,共{{ page.num_pages }}页
        # </span> {% if page.has_next %}
        # <a href="?page={{ contacts.next_page_number }}">后一页</a> {% endif %}
    logging.info("items")
    page={}
    user=""
    start=int(request.args.get("start",0))
    page["start"]=start
    limit=int(request.args.get("limit",3))
    page["limit"]=limit

    db=getdb()
    objs=db.query(PartsItem)
    total=objs.count()
    page["total"]=total
    page["hasprev"]=True;
    page["hasnext"]=True;
    if(start==0):
      page["hasprev"]=False;
    else:
      page["prevStart"]=start-limit;
    if(start+limit>=total):
      page["hasnext"]=False;
    else:
      page["nextStart"]=start+limit;
    data=[]
    for rec in objs[start:start+limit]:
        data.append(rec.json())
    return render_template("parts/items.html",user=user,contacts=data,page=page)
#    urn r
#     rewepage["lcomow="]mynFte('/':
# def hello():
# F   returpage["n redir"]ect('/static/zxd/index.html')
@app.route('/')
def index():
    return redirect('/static/zxd/index.html')
# @app.route('/test')
# def test():
#     return "test"
def toPath(p):
    return {"path": os.path.relpath(p, app_root),
            "name": os.path.basename(p),
            "time": os.path.getmtime(p)*1000,
            "isdir": os.path.isdir(p),
            "size":os.path.getsize(p)}
def toLocalPath(path):
    fsPath  =  os.path.realpath(os.path.join(app_root, path))
    if os.path.commonprefix([app_root, fsPath]) != app_root:
        raise Exception("Unsafe path "+ fsPath+" is not a  sub-path  of root "+ app_root)
    return fsPath
def toWebPath(path):
    return "/static/"+path
@app.route('/fs/children/')    
def children():
    logging.info(request.args)
    p = toLocalPath(request.args["path"])
    if os.path.exists(p):
        pass
    else:
        p= toLocalPath(".")
    children = map(lambda x : os.path.join(p, x), os.listdir(p))
    children = filter(lambda x : os.path.isfile(x) or os.path.isdir(x), children) 
    children = map(lambda x : toPath(x), children)
    print(p)
    print(children,dir(children))
    dic={"path": p,"children": list(children)}
    return json.dumps(dic, ensure_ascii=False)
@app.route('/fs/parent/')    
def parent():
    logging.info(request.args)
    p = toLocalPath(request.args["path"])
    if p == app_root:
        parent = p
    else:
        parent = os.path.dirname(p)
    dic=toPath(parent)
    return json.dumps(dic, ensure_ascii=False)
@app.route('/fs/content/')    
def content():
    p = toWebPath(request.args["path"])
    return redirect(p)
@app.route('/fs/remove/')
def remove():
    p = toLocalPath(request.args["path"])
    if os.path.isdir(p):
        shutil.rmtree(p)
    else:
        os.remove(p)
    return json.dumps({"status":"success"}, ensure_ascii=False)
@app.route('/fs/rename2/')    
def rename2():
    logging.info("rename==============")
    p = toLocalPath(request.args["path"])
    name = request.args["name"]
    parent = os.path.dirname(p)
    updated = os.path.join(parent, name)
    os.rename(p, updated)
    return json.dumps({"status":"success"}, ensure_ascii=False)
@app.route('/fs/upload/')    
def upload():
    p = toLocalPath(request.args["path"])

    name = request.args["name"]
    pweb = toWebPath(request.args["path"])+"/"+name
    uploaded = request.files['file']
    data=uploaded.read()
    uploadedPath = os.path.join(p, name)
    try:
        f = open(uploadedPath, 'wb' ) # Writing in binary mode for windows..?
        f.write( data )
        f.close( )
        res={"status":"success", "files":"./"+pweb}
    except e:
        res={"status":"fail", "files":str(e)}
    return json.dumps(res, ensure_ascii=False)
@app.route('/fs/mkdir/')
def mkdir(request):
    p = toLocalPath(request.args["path"])
    name = request.args["name"]
    os.mkdir(os.path.join(p, name))
    return HttpResponse(    json.dumps({"status":"success"}, ensure_ascii=False) ) 
@app.route('/sql/', methods=['GET'])
def sql():
    db=getdb()
    logging.info(dir(db))
    start=request.args.get("query","")
    logging.info("query")
    r=db.execute(start)
    logging.info(r)
    fs=r.keys()
    try:
        res=r.fetchall()
    except sqlalchemy.exc.ResourceClosedError as e:
        res=[]
        pass
    db.commit()#commit to avoid database is locked
    data=[]
    for one in res:
        dic1={}
        i=0
        for k in fs:
            dic1[k]=one[i]
            i+=1
        data.append(dic1)
    total=len(data)
    output={"total":total,"data":data}
    return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
@app.route('/rest/Contact/', methods=['POST', 'GET','PUT','DELETE'])
def Contact():
    logging.info("Contact==================")
    if request.method == 'GET':
        return view_contact()
    if request.method == 'POST':
        return create_contact()
    if request.method == 'PUT':
        return update_contact()
    if request.method == 'DELETE':
        return destroy_contact()        
def view_contact():
    # if session.get('db')==None:
    #     session['db']=backend_alchemy.getSession()
    start=int(request.args.get("start","0"))
    limit=int(request.args.get("limit","5"))
    search=request.args.get("search",'')
    baoxiang=request.args.get("baoxiang",'')
    logging.info("search="+search)
    logging.info("baoxiang="+baoxiang)
    db=getdb()
    objs=backend_alchemy.getContacts(db,search,baoxiang)
    total=objs.count()
    data=[]
    for rec in objs[start:start+limit]:
        data.append(rec.json())
    logging.info(data)
    output={"total":total,"data":data}
    return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
def create_contact():
        logging.info(request)
        db_session=getdb()
        
    # try:
        # logging.info(request.body)
        #data = request.form#json.loads(request.body.decode("utf-8"))#extjs read data from body
        data = json.loads(request.get_data().decode("utf-8"))
        rec=PartsContact()
        if data.get("hetongbh")!=None:
            rec.hetongbh=data["hetongbh"]
        if data.get("yujifahuo_date")!=None:
            dt=datetime.datetime.strptime(data["yujifahuo_date"],'%Y-%m-%d')
            rec.yujifahuo_date=dt.date()
        if data.get("yonghu")!=None:
            rec.yonghu=data.get("yonghu")
        if data.get("baoxiang")!=None:
            rec.baoxiang=data.get("baoxiang")
        if data.get("yiqixinghao")!=None:
            rec.yiqixinghao=data.get("yiqixinghao")
        if data.get("yiqibh")!=None:
            rec.yiqibh=data.get("yiqibh")
        if data.get("shenhe")!=None:
            rec.shenhe=data.get("shenhe")
        if data.get("addr")!=None:
            rec.addr=data.get("addr")
        if data.get("channels")!=None:
            rec.channels=data.get("channels")
        if data.get("tiaoshi_date")!=None:
            #rec.tiaoshi_date=datetime.datetime.fromtimestamp(int(data["tiaoshi_date"]))
            dt=datetime.datetime.strptime(data["tiaoshi_date"],'%Y-%m-%d')
            rec.tiaoshi_date=dt.date()
        # rec.save()
        db_session.add(rec)
        db_session.commit()
        output={"success":True,"message":"Created new User" +str(rec.id)}
        output["data"]={"id":rec.id,"shenhe":rec.shenhe,"hetongbh":rec.hetongbh,"yiqibh":rec.yiqibh,"yiqixinghao":rec.yiqixinghao,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang,"addr":rec.addr,"channels":rec.channels,"tiaoshi_date":rec.tiaoshi_date}
        return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
    # except ValueError as e:
    #     info = sys.exc_info()
    #     message=""
    #     for file, lineno, function, text in traceback.extract_tb(info[2]):
    #         message+= "%s line:, %s in %s: %s" % (file,lineno,function,text)
    #     message+= "** %s: %s" % info[:2]
    #     output={"success":False,"message":message}
    #     return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
    # except :
    #     info = sys.exc_info()
    #     message=""
    #     for file, lineno, function, text in traceback.extract_tb(info[2]):
    #         message+= "%s line:, %s in %s: %s" % (file,lineno,function,text)
    #     message+= "** %s: %s" % info[:2]
    #     output={"success":False,"message":message}
    #     return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
def update_contact():

    # data = json.loads(request.body.decode("utf-8"))#extjs read data from body
    data = json.loads(request.get_data().decode("utf-8"))
    id1=data.get("id")
    id1=int(id1)
    db_session=getdb()
    rec=db_session.query(PartsContact).filter(PartsContact.id == id1).one()
    # rec=Contact.objects.get(id=id1)
    if data.get("hetongbh")!=None:
        rec.hetongbh=data["hetongbh"]
    if data.get("yujifahuo_date")!=None:
        dt=datetime.datetime.strptime(data["yujifahuo_date"],'%Y-%m-%d')
        rec.yujifahuo_date=dt.date()
    if data.get("yonghu")!=None:
        rec.yonghu=data.get("yonghu")
    if data.get("baoxiang")!=None:
        rec.baoxiang=data.get("baoxiang")
    if data.get("yiqixinghao")!=None:
        rec.yiqixinghao=data.get("yiqixinghao")
    if data.get("yiqibh")!=None:
        rec.yiqibh=data.get("yiqibh")
    if data.get("shenhe")!=None:
        rec.shenhe=data.get("shenhe")
    if data.get("addr")!=None:
        rec.addr=data.get("addr")
    if data.get("channels")!=None:
        rec.channels=data.get("channels")
    if data.get("tiaoshi_date")!=None:
        dt=datetime.datetime.strptime(data["tiaoshi_date"],'%Y-%m-%d')
        rec.tiaoshi_date=dt.date()
    if data.get("method")!=None:
        rec.method=data["method"]
    db_session.commit()
    output={"success":True,"message":"update Contact " +str(rec.id)}
    output["data"]={"id":rec.id,"shenhe":rec.shenhe,"hetongbh":rec.hetongbh,"yiqibh":rec.yiqibh,"yiqixinghao":rec.yiqixinghao,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang,"addr":rec.addr,"channels":rec.channels,"tiaoshi_date":rec.tiaoshi_date}
    return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
def destroy_contact():
    data = json.loads(request.get_data().decode("utf-8"))
    id=data.get("id")
    if id!=None:
        try:
            id1=int(id)
            db_session=getdb()
            rec=db_session.query(PartsContact).filter(PartsContact.id == id1).one()
            db_session.delete(rec)
            db_session.commit()
            output={"success":True,"message":"OK"}
            return json.dumps(output, ensure_ascii=False)
        except ObjectDoesNotExist as e:
            output={"success":False,"message":str(e)}
            return json.dumps(output, ensure_ascii=False)
    else:
        output={"success":False,"message":"OK"}
        return json.dumps(output, ensure_ascii=False)
@app.route('/rest/UsePack/', methods=['POST', 'GET','PUT','DELETE'])
def UsePack():
    logging.info("UsePack==================")
    if request.method == 'GET':
        return view_usepack()
    if request.method == 'POST':
        return create_usepack()
    if request.method == 'PUT':
        return update_usepack()
    if request.method == 'DELETE':
        return destroy_usepack()         
def view_usepack():
    pass
def create_usepack():
    pass
def update_usepack():
    pass
def destroy_usepack():
    pass
@app.route('/rest/Pack/')    
def pack():
    logging.info("===================")
    logging.info(request)
    #logging.info("------------------")
    #request2=Request(request,(JSONParser(),))
    #logging.info(request2)
    if request.method == 'GET':
        return view_pack1()
    if request.method == 'POST':
        return create_pack1()
    if request.method == 'PUT':
        return update_pack1()
    if request.method == 'DELETE':
        return destroy_pack1()
def view_pack1():
    start=int(request.args.get("start","0"))
    limit=int(request.args.get("limit","20"))
    search_bh=request.args.get("search",'')
    db_session=getdb()
    if search_bh!='':
        q=db_session.query(PartsPack).filter(PartsPack.name.like("%"+search_bh+"%")).order_by(desc(PartsPack.id))
        total=q.count()
        objs =q[start:start+limit]
    else:
        q=db_session.query(PartsPack).order_by(desc(PartsPack.id))
        total=q.count()
        objs =q[start:start+limit]
    #total=Pack.objects.count()
    #objs = Pack.objects.all()[start:start+limit]
    data=[]
    for rec in objs:
        data.append({"id":rec.id,"name":rec.name})
    logging.info(data)
    out={"total":total,"data":data}
    return json.dumps(out, ensure_ascii=False,cls=MyEncoder)
def create_pack1(request):
    data = json.loads(request.body.decode("utf-8"))#extjs read data from body
    if(data.get("name")!=None):
        rec=Pack()
        rec.name=data["name"]
        rec.save()
        output={"success":True,"message":"Created new User" +str(rec.id)}
        output["data"]={"id":rec.id,"name":rec.name}
        return json.dumps(output, ensure_ascii=False,cls=MyEncoder)
    else:
        output={"success":False,"message":"No enough parameters"}
        output["data"]={}
        return json.dumps(output, ensure_ascii=False,cls=MyEncoder)

def update_pack1(request):
    data = json.loads(request.body.decode("utf-8"))#extjs read data from body
    id1=int(data["id"])
    rec=Pack.objects.get(id=id1)
    if data.get("name")!=None:
        rec.name=data["name"]
    rec.save()
    output={"success":True,"message":"update UsePack " +str(rec.id)}
    output["data"]={"id":rec.id,"name":rec.name}
    return json.dumps(output, ensure_ascii=False)
def destroy_pack1(request):
    data = json.loads(request.body.decode("utf-8"))#extjs read data from body
    #id=request.path.split("/")[-1]
    id1=int(data["id"])
    rec=Pack.objects.get(id=id1)
    rec.delete()
    output={"success":True,"message":"OK"}
    return json.dumps(output, ensure_ascii=False)
@app.route("/rest/Item/")
def item():
    logging.info("===================")
    logging.info(request)
    logging.info(dir(request))
    logging.info("------------------")
    #request2=Request(request,(JSONParser(),))
    #logging.info(request2)
    if request.method == 'GET':
        return view_item()
    if request.method == 'POST':
        return create_item()
    if request.method == 'PUT':
        return update_item()
    if request.method == 'DELETE':
        return destroy_item()    
def view_item():
    logging.info("here")
    #pack_id=int(request.args.get("pack"))
    start=int(request.args.get("start","0"))
    limit=int(request.args.get("limit","20"))
    search=request.args.get("query",'')
    db=getdb()
    if search!='':
        q=db.query(PartsItem).filter(PartsItem.name.like("%"+search+"%"))
        total=q.count()# | Q(bh__icontains=search)
        objs = q[start:start+limit]
    else:
        q=db.query(PartsItem)
        total=q.count()# | Q(bh__icontains=search)
        objs = q[start:start+limit]
    data=[]
    for rec in objs:
        data.append({"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei,"image":rec.image})
    logging.info(data)
    out={"total":total,"data":data}
    return json.dumps(out, ensure_ascii=False,cls=MyEncoder)
def create_item(request):
    data = json.loads(request.body.decode("utf-8"))
    #logging.info(data)
    #data=request.POST
    logging.info(data)
    requestPOST=data
    rec=Item()
    if requestPOST.get("bh")!=None:
        rec.bh=requestPOST["bh"]
    if requestPOST.get("name")!=None:
        rec.name=requestPOST["name"]
    if requestPOST.get("guige")!=None:
        rec.guige=requestPOST["guige"]
    if requestPOST.get("danwei")!=None:
        rec.danwei=requestPOST["danwei"]
    rec.save()
    output={"success":True,"message":"Created new User" +str(rec.id)}
    output["data"]={"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
    return HttpResponse(json.dumps(output, ensure_ascii=False))
def update_item(request):
    requestPOST = json.loads(request.body.decode("utf-8"))
    id1=int(requestPOST["id"])
    rec=Item.objects.get(id=id1)
    if requestPOST.get("bh")!=None:
        rec.bh=requestPOST["bh"]
    if requestPOST.get("name")!=None:
        rec.name=requestPOST["name"]
    if requestPOST.get("guige")!=None:
        rec.guige=requestPOST["guige"]
    if requestPOST.get("danwei")!=None:
        rec.danwei=requestPOST["danwei"]
    rec.save()
    output={"success":True,"message":"update item " +str(rec.id)}
    output["data"]={"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
    return HttpResponse(json.dumps(output, ensure_ascii=False))
    objs=User.objects.all()
    data=[]
    for rec in objs:
        data.append({"id":rec.id,"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang})
    output={"data":data}
    return HttpResponse(json.dumps(output, ensure_ascii=False))
def destroy_item(request):
    requestPOST = json.loads(request.body.decode("utf-8"))
    id1=int(requestPOST["id"])
    rec=Item.objects.get(id=id1)
    rec.delete()
    output={"success":True,"message":"OK"}
    return HttpResponse(json.dumps(output, ensure_ascii=False))

def main():
    app.run(host = '127.0.0.1',port=8000,debug=True)
if __name__ == '__main__':
    app.run()