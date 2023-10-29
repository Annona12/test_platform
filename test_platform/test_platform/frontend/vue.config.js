const { defineConfig } = require('@vue/cli-service')
// webpack.config.js
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack:{
      plugins: [
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  },
  lintOnSave:false,
  devServer: {
      open:true,
      host: '127.0.0.1',
      port: 8080, // 服务端口
      proxy: {
       '/api': {
            target: 'http://127.0.0.1:8000/api/login', //接口
            changeOrigin: true,//允许跨域
            // rewrite: (path) => path.replace(/^\/api/, ""),
            ws: true,
            pathRewrite: {
              '^/api': ''
        }
      }
    }
  }
})
