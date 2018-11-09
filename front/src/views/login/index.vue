<template>
  <div>
    <el-row>
      <el-col :span="18">
        <div class="page-inner"></div>
      </el-col>
      <el-col :span="6">
        <div class="login-box">
          <div class="login-planel">

            <el-form autoComplete="on" :model="loginForm" :rules="loginRules" ref="loginForm" label-position="top" label-width="0px">

              <h3 class="title">Welcome to vue-salt</h3>
              <el-form-item prop="username" label="用户名">
                <el-input name="username" type="text" v-model="loginForm.username" autoComplete="on" placeholder="username" />
              </el-form-item>
              <el-form-item prop="password" label="密码">
                <el-input name="password" :type="pwdType" @keyup.enter.native="handleLogin" v-model="loginForm.password" autoComplete="on"
                  placeholder="password"></el-input>
                  <span class="show-pwd" @click="showPwd"><svg-icon icon-class="eye" /></span>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" style="width:100%;margin-top:20px;" :loading="loading" @click.native.prevent="handleLogin">
                  登录
                </el-button>
              </el-form-item>
            </el-form>
            </div>
          </div>
        </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    const validateUsername = (rule, value, callback) => {
      if (value.length < 5) {
        callback(new Error('请输入正确的用户名'))
      } else {
        callback()
      }
    }
    const validatePass = (rule, value, callback) => {
      if (value.length < 5) {
        callback(new Error('密码不能小于5位'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, trigger: 'blur', validator: validateUsername }
        ],
        password: [{ required: true, trigger: 'blur', validator: validatePass }]
      },
      loading: false,
      pwdType: 'password'
    }
  },
  methods: {
    showPwd () {
      if (this.pwdType === 'password') {
        this.pwdType = ''
      } else {
        this.pwdType = 'password'
      }
    },
    handleLogin () {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store
            .dispatch('LoginByUsername', this.loginForm)
            .then(() => {
              this.loading = false
              this.$message({
                message: '登录成功！',
                type: 'success'
              })
              this.$router.push({ path: '/' })
            })
            .catch(() => {
              this.loading = false
              this.$message.error('登录失败，请检查用户名或密码！')
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.page-inner {
  background: url(/static/login_bg/city.jpg);
  background-size: cover;
  min-height: 988px !important;
  height: 100%;
  width: 100%;
}
.login-box {
  border-radius: 0 !important;
  padding: 80px;
  height: 988px;
  background: #fff;
  border: 1px solid #e2e2e2;
}
.login-planel {
  margin-top: 150px;
}
.title {
  display: block;
  margin-bottom: 30px;
  font-size: 30px;
  text-decoration: none;
  color: #8491a6;
  text-align: center;
}
.show-pwd {
  position: absolute;
  right: 10px;
  top: 7px;
  font-size: 16px;
  cursor: pointer;
  user-select:none;
}
</style>
