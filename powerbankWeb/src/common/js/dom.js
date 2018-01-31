
export function formatList (options) {
	let newOptions = []
	let len = options[0][0].length
	for (let i = 0; i < options.length; i++) {
		let obj = {}

		obj['value'] = options[i][0]
		obj['label'] = options[i][1]

		if (options[i][2] === false) {
			obj['children'] = []
		}
		if (i === 0) {
			newOptions.push(obj)
		} else {
			let index = options[i][0].substring(len + 1).split('.')
			if (index.length === 1) {
				newOptions[0]['children'].push(obj)
			} else {
				let cloneNewOp = newOptions[0]['children']
				for (let j = 0; j < index.length - 1; j++) {
					cloneNewOp = cloneNewOp[index[j] - 1]['children']
				}
				cloneNewOp.push(obj)
			}
		}
	}
	return newOptions
}

export function formatPowerList (data1, data2) {
	let newData = []
	for (let i = 0; i < data1.length; i++) {
		let obj = {}
		obj['id'] = data1[i][0]
		obj['label'] = data1[i][1]
		if (data2.indexOf(data1[i][0]) !== -1) {
			obj['disabled'] = false
		} else {
			obj['disabled'] = true
		}
		if (data1[i][2] === false) {
			obj['children'] = []
		}
		if (data1[i][0] !== '0') {
			let index = data1[i][0].substring(2).split('.')
			if (index.length === 1) {
				newData.push(obj)
			} else {
				let cloneNewOp = newData
				for (let j = 0; j < index.length - 1; j++) {
					cloneNewOp = cloneNewOp[index[j] - 1]['children']
				}
				cloneNewOp.push(obj)
			}
		}
	}
	return newData
}

export function comparePipe (prop) {
	return (a, b) => {
		let v1 = a[prop]
		let v2 = b[prop]
		if (v1.length === v2.length) {
			v1 = v1.split('.')
			v2 = v2.split('.')
			for (let i = 0; i < v1.length; i++) {
				if (v1[i] - v2[i] !== 0) {
					return v2[i] - v1[i]
				}
			}
		} else if (v1.length < v2.length) {
			return 1
		} else {
			return -1
		}
	}
}

export function msgNotice (msg, type, html, close, that) {
	that.$message({
		message: msg,
		type: type,
		dangerouslyUseHTMLString: html,
    showClose: close
  })
}
