import axios from 'axios'
import {commonParams} from './config'

export function logout (url) {
	const data = Object.assign({}, commonParams, {
		format: 'json'
	})

	return axios.get(url, data).then((res) => {
		return Promise.resolve(res.data)
	})
}
