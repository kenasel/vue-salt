// import { fetchUnreadMessages } from '@/api/users'
// import Cookies from 'js-cookie'

// const app = {
//   state: {
//     sidebar: {
//       opened: !+Cookies.get('sidebarStatus')
//     },
//     language: Cookies.get('language') || 'zh',
//     messages_bar: false,
//     messages_num: 0
//   },
//   mutations: {
//     TOGGLE_SIDEBAR: state => {
//       if (state.sidebar.opened) {
//         Cookies.set('sidebarStatus', 1)
//       } else {
//         Cookies.set('sidebarStatus', 0)
//       }
//       state.sidebar.opened = !state.sidebar.opened
//     },
//     TOGGLE_MESSAGES_BAR: state => {
//       state.messages_bar = !state.messages_bar
//     },
//     ADD_MESSAGES_NUM: state => {
//       state.messages_num = state.messages_num + 1
//     },
//     MIN_MESSAGES_NUM: state => {
//       state.messages_num = state.messages_num - 1
//     },
//     SET_LANGUAGE: (state, language) => {
//       state.language = language
//       Cookies.set('language', language)
//     },
//     SET_MESSAGES_NUM: (state, num) => {
//       state.messages_num = num
//     }
//   },
//   actions: {
//     toggleSideBar({ commit }) {
//       commit('TOGGLE_SIDEBAR')
//     },
//     toggleMessagesBar({ commit }) {
//       commit('TOGGLE_MESSAGES_BAR')
//     },
//     addMessagesNum({ commit }) {
//       commit('ADD_MESSAGES_NUM')
//     },
//     minMessagesNum({ commit }) {
//       commit('MIN_MESSAGES_NUM')
//     },
//     setLanguage({ commit }, language) {
//       commit('SET_LANGUAGE', language)
//     },
//     getMessagesInfo({ commit, state }) {
//       return new Promise((resolve, reject) => {
//         fetchUnreadMessages().then(response => {
//           const num = response.data.data.length
//           commit('SET_MESSAGES_NUM', num)
//           resolve(response)
//         }).catch(error => {
//           reject(error)
//         })
//       })
//     }
//   }
// }

// export default app
