<template>
    <div class="layout-class" >
      <div class="logo">
        <LogoTitle></LogoTitle>
      </div>
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

import LogoTitle from './LogoTitle/index'


export default {
  components:{
    MyMenu,
    Content,
    Header,
    LogoTitle
  }
}
</script>

<style lang="less" scoped>
.logo{
  position: fixed;
  top: 0;
  left: 0px;
  height: 60px;
  width: 200px;
  //background: #f555db;
  //border: 1px solid;
}
.menu {
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  width: 200px;
  background: #112f50;
  border: 1px solid;
}
.header{
  position: fixed;
  top: 0;
  left: 200px;
  right: 0;
  height: 55px;
  border: 1px solid;
  //background: #f134af;
}
.content {
  position: fixed;
  left: 200px;
  top:60px;
  right: 0;
  bottom: 0;
  border: 1px solid;
  //background-color: #42b983;
}
</style>