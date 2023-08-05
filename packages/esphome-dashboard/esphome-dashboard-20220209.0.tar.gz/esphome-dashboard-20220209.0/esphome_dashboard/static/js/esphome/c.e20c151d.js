import{_ as o,c as t,n as i,s as e,$ as n,Q as s,D as c}from"./index-f6fdac20.js";import"./c.ce9c6217.js";import"./c.07b1c733.js";let a=class extends e{render(){return n`
      <esphome-process-dialog
        .heading=${`Clean ${this.configuration}`}
        .type=${"clean"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){s(this.configuration)}_openInstall(){c(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],a.prototype,"configuration",void 0),a=o([i("esphome-clean-dialog")],a);
