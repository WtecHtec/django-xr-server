// components/xr-start/index.js
Component({
	/**
	 * 组件的属性列表
	 */
	properties: {

	},

	/**
	 * 组件的初始数据
	 */
	data: {
		errNum: 0,
	},

	lifetimes: {
		attached() {
			const sys = wx.getSystemInfoSync();
			if (sys.platform == 'devtools') {
				wx.showModal({
					title: '提示',
					content: '开发工具上不支持AR，请使用手机预览。',
					showCancel: false,
				});
				this.isDev = true;
			}
		},
		detached() {

		}
	},

	/**
	 * 组件的方法列表
	 */
	methods: {
		/** 初始化3d 场景要素  */
		handleReady({ detail }) {
			if (!detail.value) return;
			this.scene = detail.value;
			const xrFrameSystem = wx.getXrFrameSystem();
			this.camera = this.scene.getElementById('camera').getComponent(xrFrameSystem.Camera);
			// this.helmet = { el: this.scene.getElementById('helmet'), color: 'rgba(44, 44, 44, 0.5)' };
			// this.miku = { el: this.scene.getElementById('miku'), color: 'rgba(44, 44, 44, 0.5)' };
			this.tmpV3 = new (xrFrameSystem.Vector3)();
			console.log(this.scene)
		},

		handleAssetsLoaded({ detail }) {
			// wx.showToast({ title: '点击屏幕放置' });
			console.log('模型加载完毕')
			if (this.scene) {
				this.scene.event.add('touchstart', () => {
					this.scene.ar.placeHere('setitem', true);
				});
			}
		},
		handleTick() {
			if (this.isDev === true) {
				return
			}
			const that = this
			if (this.scene && this.camera) {
				if (this.isRefresh || this.data.errNum > 5) {
					return
				}
				if (!this.request) {
					setTimeout(() => {
						this.request = true
					}, 5 * 1000)
					return
				}
				this.isRefresh = true
				console.log(this.camera.far)
				const base64 = this.scene.share.captureToDataURL({ type: 'jpg', });
				wx.request({
					url: 'http://192.168.1.6:8080/minixr/ocr', //仅为示例，并非真实的接口地址
					data: {
						file: base64.split('base64,').pop(),
						type: 'base64'
					},
					method: 'POST',
					header: {
						'content-type': 'application/json' // 默认值
					},
					success(res) {
						const data = res.data
						console.log(data)
						setTimeout(() => {
							that.data.errNum += 1
							that.isRefresh = false
						}, 5 * 1000)
					},
					fail(err) {
						setTimeout(() => {
							that.isRefresh = false
							that.data.errNum += 1
						}, 5 * 1000)
						console.error('ocr 失败', err)
					}
				})
				// this.scene.share.captureToLocalPath({ type: 'jpg', }, (localPath) => {
				// 	console.log(localPath)
				// 	wx.uploadFile({
				// 		url: 'http://192.168.1.6:4299/minixr/ocr', //仅为示例，非真实的接口地址
				// 		filePath: localPath,
				// 		name: 'file',
				// 		formData: {},
				// 		success(res) {
				// 			const data = res.data
				// 			console.log(data)
				// 			setTimeout(() => {
				// 				this.isRefresh = true
				// 			}, 5 * 1000)
				// 			//do something
				// 		},
				// 		fail(err) {
				// 			setTimeout(() => {
				// 				this.isRefresh = true
				// 				this.data.errNum += 1
				// 			}, 5 * 1000)
				// 			console.error('ocr 失败', err)
				// 		}
				// 	})
				// });
			}
		},
	}
})
