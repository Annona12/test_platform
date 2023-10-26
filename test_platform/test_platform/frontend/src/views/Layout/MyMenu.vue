<template>
<div class="menu">
  <el-menu active-text-color="#ffd04b" background-color="#001529" class="el-menu-vertical-demo" :default-active="route.path" text-color="#ffffff" :collapse="isClose" router>
    <el-menu-item><template #title><span>自动化测试平台</span></template></el-menu-item>
    <el-menu-item index="/"><el-icon><House /></el-icon><template #title>首页管理</template></el-menu-item>
    <el-sub-menu index="/users">
      <template #title>
        <el-icon><Grid /></el-icon>
        <span>自动化管理</span>
      </template>
      <el-menu-item-group>
        <template #title><span>接口自动化</span></template>
        <el-menu-item index="/users/list">接口报文管理</el-menu-item>
        <el-menu-item index="/users/info">接口用例管理</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
    <el-sub-menu index="/users1">
      <template #title>
        <el-icon><Grid /></el-icon>
        <span>自动化管理</span>
      </template>
      <el-menu-item-group>
        <template #title><span>接口自动化</span></template>
        <el-menu-item index="/users/list">接口报文管理</el-menu-item>
        <el-menu-item index="/users/info">接口用例管理</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
  </el-menu>
</div>
</template>

<script>
import {useRoute} from 'vue-router'
export default {
  // 从父组件获取isClose开关
  props:['isClose'],
  setup(){
    // 获取当前路由的路径，后续刷新的时候自动定位到该页面
    const route = useRoute()
    return {
      route
    }

  }
}
</script>

<style scoped>
.el-menu{
border-right: none;
}

</style>