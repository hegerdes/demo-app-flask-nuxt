<!-- Please remove this file from your project -->
<template>
  <div class="relative flex items-top justify-center min-h-screen bg-gray-100 sm:items-center sm:pt-0">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.1.2/dist/tailwind.min.css" rel="stylesheet" />
    <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
      <a class="flex justify-center pt-8 sm:pt-0" href="https://nuxtjs.org" target="_blank">
        <img src="https://miro.medium.com/max/1400/1*K_EttppoSnzla46m-ZkscA.jpeg">
      </a>
      <div class="mt-8 bg-white overflow-hidden shadow sm:rounded-lg p-6">
        <h2 class="text-2xl leading-7 font-semibold text-center">
          Welcome to the <em>CLOUD</em>
        </h2>
        <div class="text-center py-4">
          <b-button @click="get">GET REQUEST</b-button>
          <b-button @click="post" variant="success">POST REQUEST</b-button>
        </div>
        <div class="text-center py-4">
          <b-button v-b-toggle.collapse-1 variant="primary">OIDC Request</b-button>
          <b-collapse id="collapse-1" class="my-2">
            <b-card>
              <b-button size="sm" class="my-2" @click="oidc">Send Request</b-button>
              <div>
                <b-form-textarea id="textarea" v-model="oidc_payload" :placeholder="demo_oidc_payload"
                  :state="oidc_validation" rows="6"></b-form-textarea>
              </div>
            </b-card>
          </b-collapse>
        </div>
        <b-table striped hover :items="tabledata"></b-table>
        <h2 class="text-2xl text-center">Raw Response</h2>
        <b-card>
          {{ data }}
        </b-card>
        <h3 class="text-2xl leading-7 font-semibold text-center">
          Provided by {{ maintainer }}
        </h3>
      </div>
      <div class="flex justify-center pt-4 space-x-2">
        <a href="https://github.com/nuxt/nuxt.js" target="_blank"><svg class="w-6 h-6 text-gray-600 hover:text-gray-800"
            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img"
            width="32" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24">
            <path
              d="M12 2.247a10 10 0 0 0-3.162 19.487c.5.088.687-.212.687-.475c0-.237-.012-1.025-.012-1.862c-2.513.462-3.163-.613-3.363-1.175a3.636 3.636 0 0 0-1.025-1.413c-.35-.187-.85-.65-.013-.662a2.001 2.001 0 0 1 1.538 1.025a2.137 2.137 0 0 0 2.912.825a2.104 2.104 0 0 1 .638-1.338c-2.225-.25-4.55-1.112-4.55-4.937a3.892 3.892 0 0 1 1.025-2.688a3.594 3.594 0 0 1 .1-2.65s.837-.262 2.75 1.025a9.427 9.427 0 0 1 5 0c1.912-1.3 2.75-1.025 2.75-1.025a3.593 3.593 0 0 1 .1 2.65a3.869 3.869 0 0 1 1.025 2.688c0 3.837-2.338 4.687-4.563 4.937a2.368 2.368 0 0 1 .675 1.85c0 1.338-.012 2.413-.012 2.75c0 .263.187.575.687.475A10.005 10.005 0 0 0 12 2.247z"
              fill="currentColor" />
          </svg></a>
        <a href="https://twitter.com/nuxt_js" target="_blank"><svg class="w-6 h-6 text-gray-600 hover:text-gray-800"
            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img"
            width="32" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24">
            <path
              d="M22.46 6c-.77.35-1.6.58-2.46.69c.88-.53 1.56-1.37 1.88-2.38c-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29c0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15c0 1.49.75 2.81 1.91 3.56c-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07a4.28 4.28 0 0 0 4 2.98a8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21C16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56c.84-.6 1.56-1.36 2.14-2.23z"
              fill="currentColor" />
          </svg></a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: '',
      tabledata: [],
      oidc_payload: "",
      demo_oidc_payload: JSON.stringify({
        "url": "https://graph.microsoft.com/v1.0/me",
        "headers": {},
        "method": "GET",
        "data": {}
      }, null, 2),
      backend: process.env.BACKEND_URL,
      maintainer: process.env.MAINTAINER,
    }
  },
  computed: {
    oidc_validation () {
      if (this.oidc_payload.length === 0) return true
      try {
        JSON.parse(this.oidc_payload);
      } catch (e) {
        return false;
      }
      return true;
    }
  },
  methods: {
    oidc: function () {
      fetch(this.backend + "/oidc", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.oidc_payload),
      })
        .then((res) => res.json())
        .then((jsonres) => {
          this.data = jsonres
          console.log(jsonres)
        })
        .catch((err) => (this.data = err))
    },
    get: function () {
      fetch(this.backend)
        .then((res) => res.json())
        .then((jsonres) => {
          this.data = jsonres
          let res_info = jsonres.RequestInfo
          res_info.RequestCounter = jsonres.ServerInfo.RequestCounter
          res_info.Node = jsonres.ServerInfo.Node
          this.tabledata.unshift(res_info)
          console.log(this.tabledata)
        })
        .catch((err) => (this.data = err))
    },

    post: function () {
      fetch(this.backend, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: 'Hello from POST' }),
      })
        .then((res) => res.json())
        .then((jsonres) => {
          this.data = jsonres
          let res_info = jsonres.RequestInfo
          res_info.RequestCounter = jsonres.ServerInfo.RequestCounter
          res_info.Node = jsonres.ServerInfo.Node
          this.tabledata.unshift(res_info)
          console.log(this.tabledata)
        })
        .catch((err) => (this.data = err))
    },
  },
}
</script>
