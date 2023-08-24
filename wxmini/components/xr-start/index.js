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
			this.helmet = { el: this.scene.getElementById('helmet'), color: 'rgba(44, 44, 44, 0.5)' };
			this.miku = { el: this.scene.getElementById('miku'), color: 'rgba(44, 44, 44, 0.5)' };
			this.tmpV3 = new (xrFrameSystem.Vector3)();
		},

		handleAssetsLoaded({ detail }) {
			wx.showToast({ title: '点击屏幕放置' });
			if (this.scene) {
				this.scene.event.add('touchstart', () => {
					this.scene.ar.placeHere('setitem', true);
				});
			}

		}
	}
})