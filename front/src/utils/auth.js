import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'

export function getToken () {
  return Cookies.get(TokenKey)
}

export function setToken (token) {
  return Cookies.set(TokenKey, token + '|' + '+0$+1s%(o%3**-c&s$08z&+z7tgc(lbwk)%l+wsh4a1%33@5%y')
}

export function removeToken () {
  return Cookies.remove(TokenKey)
}
