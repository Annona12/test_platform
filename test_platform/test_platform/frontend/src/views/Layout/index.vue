<template>
    <div class="layout-class" >
      <div class="menu">
        <MyMenu></MyMenu>
      </div>
      <div class="header">
        <Header></Header>
      </div>
      <div class="content">
        <Content></Content>
      </div>
    </div>
</template>
<script>
import MyMenu from './MyMenu'
import Content from './Content'
import Header from './Header'



export default {
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
  background: #112f50;
}
//.header{
//  //position: fixed;
//  //top: 0;
//  ////left: 200px;
//  //right: 0;
//  //height: 55px;
//  //border: 1px solid;
//  //background: #f134af;
//}
//.content {
//  //position: fixed;
//  ////left: 200px;
//  //top:60px;
//  //right: 0;
//  //bottom: 0;
//  //border: 1px solid;
//  //background-color: #42b983;
//}
</style>