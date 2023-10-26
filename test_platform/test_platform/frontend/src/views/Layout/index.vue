<template>
    <div class="layout-class" >
      <div class="menu">
        <MyMenu :isClose="isClose"></MyMenu>
      </div>
      <div class="header" >
        <Header :isClose="isClose" @change="change"></Header>
      </div>
      <div class="content" :class="{active:isClose}">
        <Content ></Content>
      </div>
    </div>
</template>
<script>
import MyMenu from './MyMenu'
import Content from './Content'
import Header from './Header'
import { ref } from 'vue';



export default {
  setup(){
    let isClose = ref(false)
    // 修改变量
    const change = () => {
        isClose.value= !isClose.value
    }
    return{
      isClose,
      change
    }
  },
  components:{
    MyMenu,
    Content,
    Header,
  }
}
</script>

<style lang="less" scoped>
.menu {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  background: #001529;
}

//.content {
//  position: fixed;
//  left: 163px;
//  top:60px;
//  right: 0;
//  bottom: 0;
//}
//.active{
//    left: 50px;
//}
//h1,
//h2,
//h3,
//p,
//ul,
//li {
//    margin: 0;
//    padding: 0;
//}
//
//a {
//    text-decoration: none;
//}
//
//ul {
//    list-style: none;
//}
</style>