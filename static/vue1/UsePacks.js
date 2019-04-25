import Client from './Client_fetch.js';
let template=`<div class="container">
     <table  class="table-bordered">
    　<thead>
    　　<tr>
    　　　 <td>ID</td>
         <td>包名称</td>
         <td >合同</td>
         <td >包</td>
         <td>操作</td>
    　　</tr>
    　</thead> 
     <tbody id="usepack-list">
                <tr v-for="(usepack,index) in usepacks">
                  <td>{{ usepack.id }}</td>
                  <td>{{ usepack.name }}</td>
                  <td>{{ usepack.hetongbh }}</td>
                  <td>{{ usepack.pack }}</td>
                  <td>
                    <button v-on:click="edit_usepack"  v-bind:index="index">编辑</button>
                    <button v-on:click="delete_usepack"  v-bind:index="index">删除</button>
                  </td>
                </tr>
      </tbody>
      </table>
      <div style="padding: 5px 5px 50px 5px;min-height:300px">  <!-- leave margin to show autocomplete items -->
      <p><input id="auto_pack1" placeholder="输入包"></p>
      <p><input id="new_pack1"  placeholder="新包"><button class="btn btn-info" id="id_new_usepack">新包</button></p>
      </div>
  </div>`;
Vue.component('usepacks', {
  template: template,
  props: ['contact'],
  name:'usepacks',
  created: function() {
    this.load_data();
  },
  data:function(){
    return {
      bg:'#ffffff',
      mydata:"",
      usepacks: [],
    };
  },
  watch: {
    old: function (val) {
      this.mydata=val;
    },
    mydata:function(val){
      if(val===this.old){
        this.bg='#ffffff'
      }
      else{
        this.bg='#8888ff'
      }
    },
  },  
  methods: {
    edit_usepack:function() {
      // body...
    },
    delete_usepack:function(){

    },
    load_data: function() {
      Client.UsePacks(
        this.contact.id,
        res => {
          console.log(res);
          this.usepacks=res.data;
        },
        function() {}
      );
  },  
}
})
export default {};