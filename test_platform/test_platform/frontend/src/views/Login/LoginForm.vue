<template>
<div>
    <el-menu
    default-active="1"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="1">密码登录</el-menu-item>
    <el-menu-item index="2">短信登录</el-menu-item>
    <el-menu-item index="3">扫码登录</el-menu-item>
  </el-menu>
</div>
  <div class="wrapper">
      <router-view />
  </div>
</template>

<script>
export default {
  name: "login_form"
}
</script>

<style scoped>

</style>