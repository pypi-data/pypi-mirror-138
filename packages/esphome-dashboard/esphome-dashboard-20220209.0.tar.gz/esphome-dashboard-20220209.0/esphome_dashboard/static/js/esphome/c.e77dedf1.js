import{r as t,_ as o,c as e,f as s,n as i,s as a,$ as r,Q as n}from"./index-f6fdac20.js";import"./c.ce9c6217.js";import{o as c}from"./c.ce02c2d6.js";import"./c.07b1c733.js";import"./c.04217849.js";import"./c.3b677cd8.js";import"./c.3f3af8e3.js";import"./c.d4a4f0e7.js";let l=class extends a{render(){return r`
      <esphome-process-dialog
        .heading=${`Install ${this.configuration}`}
        .type=${"upload"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${"OTA"===this.target?"":r`
              <a
                href="https://esphome.io/guides/faq.html#i-can-t-get-flashing-over-usb-to-work"
                slot="secondaryAction"
                target="_blank"
                >❓</a
              >
            `}
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){n(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};l.styles=t`
    a[slot="secondaryAction"] {
      text-decoration: none;
      line-height: 32px;
    }
  `,o([e()],l.prototype,"configuration",void 0),o([e()],l.prototype,"target",void 0),o([s()],l.prototype,"_result",void 0),l=o([i("esphome-install-server-dialog")],l);
