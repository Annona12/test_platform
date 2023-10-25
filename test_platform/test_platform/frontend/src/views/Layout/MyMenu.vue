<template>
<div class="menu">
  <el-menu active-text-color="#ffd04b" background-color="#112f50" class="el-menu-vertical-demo" default-active="1" text-color="#fff" :collapse="isCollapse" router>
    <el-menu-item><template #title><span>自动化测试平台</span></template></el-menu-item>
    <el-menu-item index="/"><template #title><el-icon><House /></el-icon><span>首页管理</span></template></el-menu-item>
    <el-sub-menu index="2">
      <template #title>
        <el-icon><Grid /></el-icon>
        <span>自动化管理</span>
      </template>
      <el-menu-item-group>
        <template #title><span>接口自动化</span></template>
        <el-menu-item index="2-1">接口报文管理</el-menu-item>
        <el-menu-item index="2-2">接口用例管理</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>

  </el-menu>
</div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup(){
    // 定义开关
    const isCollapse = ref(false)

    return {
      isCollapse
    }

  }
}
</script>

<style scoped>

/*.el-menu-vertical-demo:not(.el-menu--collapse) {*/
/*  width: 200px;*/
/*  min-height: 400px;*/
/*}*/
</style>