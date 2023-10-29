<template>
  <div id="login-page" class="both-center">
    <div class="container-news space-between hor-center">
      <div class="left">
                        <img src="../../static/img/login_left_background.png" alt="">
      </div>
      <div class="right col relative">
        <div class="col stgap4">
          <div class="title">欢迎使用自动化测试平台</div>
          <div class="col stgap3">
            <el-input placeholder="请输入用户名" v-model="account" autofocus></el-input>
            <el-input placeholder="请输入密码" v-model="password" maxlength="12" show-password></el-input>
          </div>
          <div class="col stgap2">
            <el-button style="width:100%" type="primary" :disabled="!canlogin" size="medium"
                        @click="login()">
              登录
            </el-button>
            <div class="space-between hor-center">
              <el-checkbox v-model="checked" >记住密码</el-checkbox>
              <el-button type="text">忘记密码？</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      account: '',
      password: '',
      checked: false,
      loading: false,
    }
  },
  computed: {
    canlogin() {
      if (this.account.length >=6  && this.password.length >= 8) {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    login() {
      console.log(this.account)
      console.log(this.password)
      console.log(this.checked)
      axios.get('/api'
      //     ,{
      //   username:this.account,
      //   password:this.password
      // }
      ).then({})
      console.log('登录提交')
      // if (this.account != 'joe' || this.password != '88888888') {
      //   this.$message({
      //     showClose: true,
      //     message: '账号密码有误',
      //     type: 'error',
      //     duration: 1800
      //   });
      //   return
      // }
      // this.loading = true
      // throttle(this.go,2000)
    },
    // go() {
    //   this.$message({
    //     showClose: true,
    //     message: '登录成功!',
    //     type: 'success',
    //     duration: 1800
    //   });
    //   this.$router.push('/')
    // }
  }
}
</script>

<style scoped>
#login-page {
  position: relative;
  width: 100%;
  height: 100vh;
  background: #F9F9F9;
  background-image: url('../../static/img/login_background.jpg');
  background-size: cover;
  margin: 0px;
}
.left {
  width: 571px;
  height: 571px;
}
.right {
  position: fixed;
  top: 100px;
  left: 800px;
  width: 460px;
  height: 516px;
  padding: 40px;
  border-radius: 12px;

  background: #eeecec5e;
  box-shadow: 0px 0px 4px 0px rgba(0, 0, 0, 0.08), 0px 2px 6px 0px rgba(0, 0, 0, 0.06), 0px 4px 8px 2px rgba(0, 0, 0, 0.04);
}
.title {
  font-family: HarmonyOS_Sans_SC_Bold;
  font-size: 20px;
  font-weight: bold;
  line-height: 28px;
  letter-spacing: 0px;
  color: #000000;
  text-align: center;
}
.el-input{
  margin-top:30px;
}
.el-button {
  margin-top: 30px;
}
.el-button--text {
  padding-left:390px;
  padding-top: -50px;
}
.qrcode {
  position: absolute;
  top: 0;
  right: 0;
  cursor: pointer;
}
</style>

