import axios from 'axios'
import {commonParams} from './config'

export function getData (tips, url) {
	const data = Object.assign({}, commonParams, {
		format: 'json',
		tips: tips
	})

	return axios.post(url, {
		params: data
	}).then((res) => {
		return Promise.resolve(res.data)
	})
}
