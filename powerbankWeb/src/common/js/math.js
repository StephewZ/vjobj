
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
	console.log(newOptions)
	return newOptions
}
