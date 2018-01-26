
export function formatList (options) {
	let newOptions = []
	let len = options[0][0].length
	for (let i = 1; i < options.length; i++) {
		let obj = {}

		obj['value'] = options[i][0]
		obj['label'] = options[i][1]

		if (options[i][2] === false) {
			obj['children'] = []
		}

		let index = options[i][0].substring(len + 1).split('.')
		if (index.length === 1) {
			newOptions.push(obj)
		} else {
			let cloneNewOp = newOptions
			for (let j = 0; j < index.length - 1; j++) {
				cloneNewOp = cloneNewOp[index[j] - 1]['children']
			}
			cloneNewOp.push(obj)
		}
	}
	return newOptions
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
