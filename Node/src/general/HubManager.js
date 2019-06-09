import ehealth from './i3app';
class HubManager {
    constructor() {
        this._isHubInit = false;
        this._isConnected = false;
        this._needList = new Map();
        this._needList.set("Auction", 1);
        this._needDic = new Map();
        this._listPendingRegisterNeed = [];
        this._registerClientFunction();

    };

    connectHub() {
        if (window.signalRConnection) {
            this._isHubInit = true;
            window.signalRConnection.hub.start({ transport: 'longPolling' }).done(() => {
                this.updateConnected();
                this._listPendingRegisterNeed.forEach(o => {
                    this.registerNeed(o.need, o.component, o.callback);
                });
            });
        }
    }
    updateConnected() {
        this._isConnected = true;
    }

    _needKey(need) {
        return need.need;
    }
    
    registerNeed(need, component, callback) {
        if (window.signalRConnection) {
            if (this._isConnected === false) {
                this._listPendingRegisterNeed.push({ need, component, callback });
                if (this._isHubInit === false) {
                    this.connectHub();
                }
                return;
            }
            let needDic = this._needDic;

            let needKey = this._needKey(need);
            let components = needDic.get(needKey);
            if (!components) {
                let data = {
                    connectionId: window.signalRConnection.hub.id,
                    signalRNeeds: [need]
                };
                let ajaxObject = {
                    url: '/api/event/UpdateNeed',
                    data: JSON.stringify(data),
                    successCallback: () => {
                        needDic.set(needKey, [component]);
                        if (typeof callback === 'function') {
                            callback();
                        }
                    },
                    errorCallback: null,
                    isNotBlockUI: true,
                    unsuccessFunction: null,
                }
                ehealth.ajax.post(ajaxObject);
            }
            else {
                components.push(component);
                if (typeof callback === 'function') {
                    callback();
                }
            }
        }
    };

    unregisterNeed(need, component) {
        let needDic = this._needDic;
        console.log(need);

        let data = {
            connectionId: window.signalRConnection.hub.id,
            signalRNeeds: [need]
        };
        let needKey = this._needKey(need);
        let ajaxObject = {
            url: '/api/event/RemoveNeed',
            data: JSON.stringify(data),
            successCallback: (ack) => {
                let components = needDic.get(needKey);
                if (components && components.length > 0) {
                    let componentIndex = components.indexOf(component);
                    componentIndex >= 0 && components.splice(componentIndex, 1);
                }
            },
            errorCallback: null,
            isNotBlockUI: true,
            unsuccessFunction: null,
        }
        ehealth.ajax.post(ajaxObject);
        needDic.delete(needKey);
    };

    _getListComponents(needName) {
        let need = this._needList.get(needName);
        let components = this._needDic.get(need);
        return components ? components : [];
    };

    _registerClientFunction() {
        if (window.signalRConnection) {
            let client = window.signalRConnection.eventHub.client;
            client.updateAuction = (currentWinner) => { //BidPlacing
                //message = $.ehealth.toCamel(message);
                let components = this._getListComponents("Auction");
                components.forEach(c => {
                    c.updateAuction(currentWinner);
                });
            }
            client.updateAuctionInfo = (auctionInfo) => {
                let components = this._getListComponents("Auction");
                components.forEach(c => {
                    c.updateAuctionInfo(auctionInfo);
                });
            }
        }
    }
}

export default HubManager;