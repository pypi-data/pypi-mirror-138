import{a as t,r as e,_ as i,c as o,f as s,j as a,n as r,s as d,$ as n,D as c,S as l,P as h}from"./index-f6fdac20.js";import"./c.07b1c733.js";import{c as p,s as u}from"./c.37c9c962.js";let m=class extends d{constructor(){super(...arguments),this._adopted=!1,this._busy=!1,this._cleanSSIDBlur=t=>{const e=t.target;e.value=e.value.trim()}}render(){return n`
      <mwc-dialog
        .heading=${this._adopted?"Configuration created":"Adopt device"}
        @closed=${this._handleClose}
        open
      >
        ${this._adopted?n`
              <div>
                To finish adoption, the new configuration needs to be installed
                on the device. This can be done wirelessly.
              </div>
              <mwc-button
                slot="primaryAction"
                dialogAction="install"
                label="Install"
                @click=${()=>c(`${this.device.name}.yaml`)}
              ></mwc-button>
              <mwc-button
                slot="secondaryAction"
                dialogAction="skip"
                label="skip"
              ></mwc-button>
            `:n`
              <div>
                Adopting ${this.device.name} will create an ESPHome
                configuration for this device. This allows you to install
                updates and customize the original firmware.
              </div>

              ${this._error?n`<div class="error">${this._error}</div>`:""}
              ${!1!==this._hasWifiSecrets?n`
                    <div>
                      This device will be configured to connect to the Wi-Fi
                      network stored in your secrets.
                    </div>
                  `:n`
                    <div>
                      Enter the credentials of the Wi-Fi network that you want
                      your device to connect to.
                    </div>
                    <div>
                      This information will be stored in your secrets and used
                      for this and future devices. You can edit the information
                      later by editing your secrets at the top of the page.
                    </div>

                    <mwc-textfield
                      label="Network name"
                      name="ssid"
                      required
                      @blur=${this._cleanSSIDBlur}
                      .disabled=${this._busy}
                    ></mwc-textfield>

                    <mwc-textfield
                      label="Password"
                      name="password"
                      type="password"
                      helper="Leave blank if no password"
                      .disabled=${this._busy}
                    ></mwc-textfield>
                  `}

              <mwc-button
                slot="primaryAction"
                .label=${this._busy?"Adopting…":"Adopt"}
                @click=${this._handleAdopt}
                .disabled=${void 0===this._hasWifiSecrets}
              ></mwc-button>
              ${this._busy?"":n`
                    <mwc-button
                      no-attention
                      slot="secondaryAction"
                      label="Cancel"
                      dialogAction="cancel"
                    ></mwc-button>
                  `}
            `}
      </mwc-dialog>
    `}firstUpdated(t){super.firstUpdated(t),p().then((t=>{this._hasWifiSecrets=t}))}_handleClose(){this.parentNode.removeChild(this)}async _handleAdopt(){if(this._error=void 0,!1===this._hasWifiSecrets){if(!this._inputSSID.reportValidity())return void this._inputSSID.focus();this._busy=!0;try{await u(this._inputSSID.value,this._inputPassword.value)}catch(t){return this._busy=!1,void(this._error="Failed to store Wi-Fi credentials")}}this._busy=!0;try{await l(this.device),h(this,"adopted"),this._adopted=!0}catch(t){this._busy=!1,this._error="Failed to import device"}}};m.styles=[t,e`
      :host {
        --mdc-dialog-max-width: 390px;
      }
      .error {
        color: var(--alert-error-color);
        margin-bottom: 16px;
      }
    `],i([o()],m.prototype,"device",void 0),i([s()],m.prototype,"_hasWifiSecrets",void 0),i([s()],m.prototype,"_adopted",void 0),i([s()],m.prototype,"_busy",void 0),i([s()],m.prototype,"_error",void 0),i([a("mwc-textfield[name=ssid]")],m.prototype,"_inputSSID",void 0),i([a("mwc-textfield[name=password]")],m.prototype,"_inputPassword",void 0),m=i([r("esphome-adopt-dialog")],m);
