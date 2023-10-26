<template>
<div class="header" :class="{active:isClose}">
  <div class="icon">
    <el-icon v-if="isClose" @click="change"><Expand /></el-icon>
    <el-icon v-else @click="change"><Fold /></el-icon>
  </div>
  <div class="right">
    <div class="time">{{ time }}</div>
    <div class="line">|</div>
    <div class="loginout" @click="out"><el-icon><SwitchButton /></el-icon></div>
  </div>
  <div class="header-router">

  </div>
</div>
</template>

<script>
import { onMounted, ref } from 'vue'
import dayjs from 'dayjs'
import router from '@/router';

export default {
  props:['isClose'],
  emits: ['change'],
  setup(props,{ emit }){
    //定义时间
    let time = ref(null)
    //折叠菜单
    const change = () => {
      emit('change');
    }
    //退出登录
    const out =()=>{
      router.push('/login')
    }
    //生命周期函数
    onMounted(() => {
      //获取当前的时间
       time.value = dayjs(new Date()).format('YYYY-MM-DD HH:mm:ss')
    })
    return{
      change,
      time,
      out
    }
  },
}
</script>

<style scoped>
.header{
  position: fixed;
  top: 0;
  left: 163px;
  right: 0;
  height: 56px;
  background: #ffffff;
  align-items:center;
  border: 1px solid #efefef;
  display:flex;
}
.icon {
    font-size: 24px;
    flex: 1;
}
.active{
    left: 64px;
}
.right {
  padding-right: 20px;
  display: flex;
}
.time {
      font-size: 15px;
}
.line{
      padding-right: 10px;
      padding-left: 10px;
}
.loginout{
      margin-top: 2px;
      cursor: pointer;
}
</style>