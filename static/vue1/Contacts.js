import Client from './Client_fetch.js';
import NullContactEdit from "./ContactEdit.js";
var app = new Vue({
  template:`<div>
    <nav class="navbar navbar-dark bg-dark">
      <a class="navbar-brand" href="#">装箱单</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample01" aria-controls="navbarsExample01" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>  
        <div class="collapse navbar-collapse" id="navbarsExample01">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item"><a href="/parts/items/">备件</a></li>
            <li class="nav-item"><a href="/parts/copypack/">复制包</a></li>
          </ul>
        </div>
      </nav>
      <div class="container table-responsive">
        <div id="todoapp">
          <div>
            <table>
              <tr>
                <td>
                  <div class="dropdown">
                    <button
                      class="btn btn-default dropdown-toggle"
                      type="button"
                      id="dropdownMenu1"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="true"
                    >
                      <span id="dropdownMenu1_text">{{user}}</span>
                      <span class="caret"></span>
                    </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenu1">
                      <a class="dropdown-item" href="#" id="id_login">log in</a>
                      <a class="dropdown-item" id="id_logout">log out</a>
                    </div>
                  </div>
                </td>
                <td>
                  <input placeholder="合同 or 仪器编号" v-model="search" />
                  <button
                    v-on:click="go_search"
                    id="id_bt_search"
                    class="btm btn-info"
                  >
                    搜索
                  </button>
                  <button
                    id="id_bt_new"
                    v-on:click="edit"
                    index="null"
                    class="btn btn-primary"
                  >
                    新仪器
                  </button>
                </td>
                <td>
                  <div class="dropdown">
                    <button
                      class="btn btn-default dropdown-toggle"
                      type="button"
                      id="dropdownMenu2"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="true"
                    >
                      <span id="dropdownMenu2_text">包箱:{{baoxiang}}</span>
                      <span class="caret"></span>
                    </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenu2">
                      <a
                        class="dropdown-item"
                        href="#"
                        v-on:click="baoxiang_change"
                        >马红权</a
                      >
                      <a
                        class="dropdown-item"
                        v-on:click="baoxiang_change"
                        >陈旺</a
                      >
                      <a
                        class="dropdown-item"
                        v-on:click="baoxiang_change"
                        >吴振宁</a
                      >
                      <a
                        class="dropdown-item"
                        v-on:click="baoxiang_change"
                        ><span class="glyphicon glyphicon-asterisk"></span
                      ></a>
                    </div>
                  </div>
                </td>
              </tr>
            </table>
          </div>
          <div id="main" style="min-height:200px;">
            <table class="table-bordered">
              <thead>
                <tr>
                  <td>ID</td>
                  <td>用户单位</td>
                  <td>客户地址</td>
                  <td>通道配置</td>
                  <td>仪器型号</td>
                  <td>仪器编号</td>
                  <td>包箱</td>
                  <td>审核</td>
                  <td>预计发货时间</td>
                  <td>调试时间</td>
                  <td>合同编号</td>
                  <td>方法</td>
                </tr>
              </thead>
              <tbody id="contact-list">
                <tr v-for="(contact,index) in contacts">
                  <td>{{ contact.id }}</td>
                  <td>{{ contact.yonghu }}</td>
                  <td>{{ contact.addr }}</td>
                  <td>{{ contact.channels }}</td>
                  <td>{{ contact.yiqixinghao }}</td>
                  <td>
                    <button v-on:click="edit"  v-bind:index="index">{{ contact.yiqibh }}</button>
                    <div class="dropdown">
                      <button
                        class="btn btn-default dropdown-toggle"
                        type="button"
                        id="dropdownMenu5"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="true"
                      >
                        <span class="caret"></span>
                      </button>
                      <div
                        class="dropdown-menu"
                        aria-labelledby="dropdownMenu5"
                      >
                        <a class="dropdown-item" v-on:click="caozuo_change"
                          >详细</a
                        >
                      </div>
                    </div>
                  </td>
                  <td>{{ contact.baoxiang }}</td>
                  <td>{{ contact.shenhe }}</td>
                  <td>{{ contact.yujifahuo_date }}</td>
                  <td>{{ contact.tiaoshi_date }}</td>
                  <td>{{ contact.hetongbh }}</td>
                  <td><a>{{ contact.method }}</a></td>
                </tr>
              </tbody>
            </table>
            <button v-on:click="prev" id="bt_prev">前一页</button>
            <label id="page">{{start}}/{{total}}</label>
            <button v-on:click="next" id="bt_next">后一页</button>
          </div>

          <contact-edit ref="dlgEdit" v-bind:contact="contact" v-bind:index="currentIndex"/>
          <div style="min-height: 300px"></div>
        </div>
      </div></div>
`,
  el: '#app',
  created: function() {
    this.load_data();
  },
  methods: {
    load_data: function() {
      Client.contacts(
        {
          limit: this.limit,
          start: this.start,
          baoxiang: this.baoxiang,
          search: this.search,
        },
        res => {
          this.contacts = res.data;
          this.total = res.total;
          this.user = res.user;
          console.log(this.contacts);
        },
        function() {}
      );
    },
    prev: function() {
      this.start = this.start - this.limit;
      if (this.start < 0) {
        this.start = 0;
      }
      this.load_data();
    },
    next: function() {
      this.start = this.start + this.limit;
      if (this.start > this.total - this.limit)
        this.start = this.total - this.limit; //total >limit
      this.load_data();
    },
    go_search: function() {
      this.load_data();
    },
    baoxiang_change: function(e) {
      this.baoxiang = e.target.text;
      this.load_data();
    },
    caozuo_change: function() {
      console.log('xiangxi');
    },
    edit: function(e) {
      let v=parseInt(e.target.attributes.index.value);
      if (isNaN(v)){
        this.currentIndex=null;  
        this.contact={};
      }
      else{
        this.currentIndex=v;   
        this.contact=this.contacts[this.currentIndex]
      }
      this.$refs.dlgEdit.open();
    },
  },
  data: {
    contacts: [],
    contact: {},
    currentIndex:null,
    user: '',
    baoxiang: '',
    search: '',
    total: 0,
    start: 1,
    limit: 3,
  },
});
