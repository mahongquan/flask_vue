/////////////
import queryString from './lib/querystring/index.js';
// import myglobal from './myglobal';
// const fetch = require('node-fetch');
let host = '';
if (window.require) {
  host = 'http://127.0.0.1:8000';
}
function myFetch(method, url, body, cb, headers2, err_callback) {
  let data;
  let headers;
  if (headers2) {
    headers = headers2;
  } else {
    headers = { 'Content-Type': 'application/json' };
  }
  if (method === 'GET') {
    data = {
      method: method,
      credentials: 'include',
      headers: headers,
    };
  } else {
    data = {
      method: method,
      credentials: 'include',
      headers: headers,
      body: body,
    };
  }
  return fetch(host + url, data)
    .then(checkStatus)
    .then(parseJSON)
    .then(cb)
    .catch(err_callback)
  // return fetch(host + url, data)
  //   .then(checkStatus)
  //   .then(parseJSON)
  //   .then(cb)
  //   .catch(error => {
  //     if (err_callback) err_callback(error);
  //     else alert(error + '\n请检查服务器/刷新网页/登录');
  //   });
}
function getRaw(url, cb, err_callback) {
  return myFetch('GET', url, undefined, cb, undefined, err_callback);
}
function get(url, data, cb, err_callback) {
  url = url + '?' + queryString.stringify(data);
  console.log(url);
  return getRaw(url, cb, err_callback);
}
function delete1(url, data, cb,err_callback) {
  var method = 'DELETE';
  return myFetch(method, url, JSON.stringify(data), cb,undefined,err_callback);
}
function post(url, data, cb,err_callback) {
  var method = 'POST';
  return myFetch(method, url, JSON.stringify(data), cb,undefined,err_callback);
}
function postOrPut(url, data, cb,err_callback) {
  var method = 'POST';
  if (data.id) {
    method = 'PUT';
  }
  return myFetch(method, url, JSON.stringify(data), cb,undefined,err_callback);
}
function postForm(url, data, cb,err_callback) {
  var method = 'POST';
  return fetch(url, {
    method: method,
    credentials: 'include',
    body: data,
  })
    .then(checkStatus)
    .then(parseJSON)
    .then(cb)
    .catch(err_callback);
}
function contacts(data, cb, err_callback) {
  return get('/rest/Contact/', data, cb, err_callback);
}
function UsePacks(query, cb,err_callback) {
  var data = { contact: query };
  return get('/rest/UsePack/', data, cb,err_callback);
}
function PackItems(query, cb) {
  var data = { pack: query };
  return get('/rest/PackItem/', data, cb);
}
function items(query, cb) {
  var data = { search: query };
  return get('/rest/Item/', data, cb);
}
function sql(query, cb) {
  var data = { query: query };
  return get('/sql/', data, cb);
}

function login_index(cb) {
  return get('/rest/login', undefined, cb);
}
function logout(cb) {
  return get('/rest/logout', undefined, cb);
}

function login(username, password, cb) {
  //post form
  var payload = {
    username: username,
    password: password,
  };
  var body = queryString.stringify(payload);
  return myFetch('POST', '/rest/login', body, cb, {
    'META':'CSRF_COOKIE',
    'Content-Type': 'application/x-www-form-urlencoded',
  });
}

function checkStatus(response) {
  // let es,one;
  // es=response.headers.keys();
  // while(true){
  //   one=es.next();
  //   console.log(one.value);
  //   if(one.done) break;
  // }  
  // es=response.headers.entries();
  // while(true){
  //   one=es.next();
  //   // console.log(one.value);
  //   if(one.done) break;
  // }  
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(`HTTP Error ${response.statusText}`);
  error.status = response.statusText;
  error.response = response;
  throw error;
}

function parseJSON(response) {
  var r = response.json();
  return r;
}
const Client = {
  sql,
  init: (m, callback) => {
    callback();
  },
  getRaw,
  contacts,
  items,
  login_index,
  login,
  logout,
  UsePacks,
  PackItems,
  get,
  post,
  postOrPut,
  delete1,
  postForm,
};
export default Client;
