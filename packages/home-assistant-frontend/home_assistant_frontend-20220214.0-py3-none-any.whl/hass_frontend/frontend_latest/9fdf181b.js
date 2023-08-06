"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7065],{67065:(e,t,a)=>{var r=a(3239),i=a(37500),l=a(33310),o=a(8636),d=a(51346),c=a(70483),n=a(14516),s=a(25516),h=a(47181),m=(a(7164),a(38346)),u=a(96151),f=a(11654),_=(a(32511),a(52039),a(93217));let b;a(9874);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(a){t.forEach((function(t){t.kind===a&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var a=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var l="static"===i?e:a;this.defineClassElement(l,t)}}),this)}),this)},defineClassElement:function(e,t){var a=t.descriptor;if("field"===t.kind){var r=t.initializer;a={enumerable:a.enumerable,writable:a.writable,configurable:a.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,a)},decorateClass:function(e,t){var a=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!g(e))return a.push(e);var t=this.decorateElement(e,i);a.push(t.element),a.push.apply(a,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:a,finishers:r};var l=this.decorateConstructor(a,t);return r.push.apply(r,l.finishers),l.finishers=r,l},addElementPlacement:function(e,t,a){var r=t[e.placement];if(!a&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var a=[],r=[],i=e.decorators,l=i.length-1;l>=0;l--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var d=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[l])(d)||d);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var n=c.extras;if(n){for(var s=0;s<n.length;s++)this.addElementPlacement(n[s],t);a.push.apply(a,n)}}return{element:e,finishers:r,extras:a}},decorateConstructor:function(e,t){for(var a=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),l=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==l.finisher&&a.push(l.finisher),void 0!==l.elements){e=l.elements;for(var o=0;o<e.length-1;o++)for(var d=o+1;d<e.length;d++)if(e[o].key===e[d].key&&e[o].placement===e[d].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:a}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return C(e,t);var a=Object.prototype.toString.call(e).slice(8,-1);return"Object"===a&&e.constructor&&(a=e.constructor.name),"Map"===a||"Set"===a?Array.from(e):"Arguments"===a||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a)?C(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var a=x(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var l={kind:t,key:a,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),l.initializer=e.initializer),l},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var a=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:a}},runClassFinishers:function(e,t){for(var a=0;a<t.length;a++){var r=(0,t[a])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,a){if(void 0!==e[t])throw new TypeError(a+" can't have a ."+t+" property.")}};return e}function v(e){var t,a=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:a,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var a=e[t];if(void 0!==a&&"function"!=typeof a)throw new TypeError("Expected '"+t+"' to be a function");return a}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var a=e[Symbol.toPrimitive];if(void 0!==a){var r=a.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var a=0,r=new Array(t);a<t;a++)r[a]=e[a];return r}function R(e,t,a){return R="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,a){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=D(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(a):i.value}},R(e,t,a||e)}function D(e){return D=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},D(e)}!function(e,t,a,r){var i=p();if(r)for(var l=0;l<r.length;l++)i=r[l](i);var o=t((function(e){i.initializeInstanceElements(e,d.elements)}),a),d=i.decorateClass(function(e){for(var t=[],a=function(e){return"method"===e.kind&&e.key===l.key&&e.placement===l.placement},r=0;r<e.length;r++){var i,l=e[r];if("method"===l.kind&&(i=t.find(a)))if(y(l.descriptor)||y(i.descriptor)){if(g(l)||g(i))throw new ReferenceError("Duplicated methods ("+l.key+") can't be decorated.");i.descriptor=l.descriptor}else{if(g(l)){if(g(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+l.key+").");i.decorators=l.decorators}k(l,i)}else t.push(l)}return t}(o.d.map(v)),e);i.initializeClassElements(o.F,d.elements),i.runClassFinishers(o.F,d.finishers)}([(0,l.Mo)("ha-data-table")],(function(e,t){class p extends t{constructor(...t){super(...t),e(this)}}return{F:p,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Object})],key:"columns",value:()=>({})},{kind:"field",decorators:[(0,l.Cb)({type:Array})],key:"data",value:()=>[]},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"selectable",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"clickable",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"hasFab",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,attribute:"auto-height"})],key:"autoHeight",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:String})],key:"id",value:()=>"id"},{kind:"field",decorators:[(0,l.Cb)({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:String})],key:"searchLabel",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:String})],key:"filter",value:()=>""},{kind:"field",decorators:[(0,l.SB)()],key:"_filterable",value:()=>!1},{kind:"field",decorators:[(0,l.SB)()],key:"_filter",value:()=>""},{kind:"field",decorators:[(0,l.SB)()],key:"_sortColumn",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_sortDirection",value:()=>null},{kind:"field",decorators:[(0,l.SB)()],key:"_filteredData",value:()=>[]},{kind:"field",decorators:[(0,l.SB)()],key:"_headerHeight",value:()=>0},{kind:"field",decorators:[(0,l.IO)("slot[name='header']")],key:"_header",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_items",value:()=>[]},{kind:"field",key:"_checkableRowsCount",value:void 0},{kind:"field",key:"_checkedRows",value:()=>[]},{kind:"field",key:"_sortColumns",value:()=>({})},{kind:"field",key:"curRequest",value:()=>0},{kind:"field",decorators:[(0,s.i)(".scroller")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_debounceSearch",value(){return(0,m.D)((e=>{this._filter=e}),100,!1)}},{kind:"method",key:"clearSelection",value:function(){this._checkedRows=[],this._checkedRowsChanged()}},{kind:"method",key:"connectedCallback",value:function(){R(D(p.prototype),"connectedCallback",this).call(this),this._items.length&&(this._items=[...this._items])}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then((()=>this._calcTableHeight()))}},{kind:"method",key:"willUpdate",value:function(e){if(R(D(p.prototype),"willUpdate",this).call(this,e),e.has("columns")){this._filterable=Object.values(this.columns).some((e=>e.filterable));for(const e in this.columns)if(this.columns[e].direction){this._sortDirection=this.columns[e].direction,this._sortColumn=e;break}const e=(0,r.Z)(this.columns);Object.values(e).forEach((e=>{delete e.title,delete e.type,delete e.template})),this._sortColumns=e}e.has("filter")&&this._debounceSearch(this.filter),e.has("data")&&(this._checkableRowsCount=this.data.filter((e=>!1!==e.selectable)).length),(e.has("data")||e.has("columns")||e.has("_filter")||e.has("_sortColumn")||e.has("_sortDirection"))&&this._sortFilterData()}},{kind:"method",key:"render",value:function(){return i.dy`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?i.dy`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${(0,o.$)({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length+1}
          style=${(0,c.V)({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div class="mdc-data-table__header-row" role="row" aria-rowindex="1">
            ${this.selectable?i.dy`
                  <div
                    class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                    role="columnheader"
                  >
                    <ha-checkbox
                      class="mdc-data-table__row-checkbox"
                      @change=${this._handleHeaderRowCheckboxClick}
                      .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                      .checked=${this._checkedRows.length===this._checkableRowsCount}
                    >
                    </ha-checkbox>
                  </div>
                `:""}
            ${Object.entries(this.columns).map((([e,t])=>{if(t.hidden)return"";const a=e===this._sortColumn,r={"mdc-data-table__header-cell--numeric":"numeric"===t.type,"mdc-data-table__header-cell--icon":"icon"===t.type,"mdc-data-table__header-cell--icon-button":"icon-button"===t.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===t.type,sortable:Boolean(t.sortable),"not-sorted":Boolean(t.sortable&&!a),grows:Boolean(t.grows)};return i.dy`
                <div
                  aria-label=${t.label}
                  class="mdc-data-table__header-cell ${(0,o.$)(r)}"
                  style=${t.width?(0,c.V)({[t.grows?"minWidth":"width"]:t.width,maxWidth:t.maxWidth||""}):""}
                  role="columnheader"
                  aria-sort=${(0,d.o)(a?"desc"===this._sortDirection?"descending":"ascending":void 0)}
                  @click=${this._handleHeaderClick}
                  .columnId=${e}
                >
                  ${t.sortable?i.dy`
                        <ha-svg-icon
                          .path=${a&&"desc"===this._sortDirection?"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z":"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}
                        ></ha-svg-icon>
                      `:""}
                  <span>${t.title}</span>
                </div>
              `}))}
          </div>
          ${this._filteredData.length?i.dy`
                <lit-virtualizer
                  scroller
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                  .items=${this._items}
                  .renderItem=${this._renderRow}
                ></lit-virtualizer>
              `:i.dy`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||"No data"}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}},{kind:"field",key:"_renderRow",value(){return(e,t)=>e?e.append?i.dy` <div class="mdc-data-table__row">${e.content}</div> `:e.empty?i.dy` <div class="mdc-data-table__row"></div> `:i.dy`
      <div
        aria-rowindex=${t+2}
        role="row"
        .rowId=${e[this.id]}
        @click=${this._handleRowClick}
        class="mdc-data-table__row ${(0,o.$)({"mdc-data-table__row--selected":this._checkedRows.includes(String(e[this.id])),clickable:this.clickable})}"
        aria-selected=${(0,d.o)(!!this._checkedRows.includes(String(e[this.id]))||void 0)}
        .selectable=${!1!==e.selectable}
      >
        ${this.selectable?i.dy`
              <div
                class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                role="cell"
              >
                <ha-checkbox
                  class="mdc-data-table__row-checkbox"
                  @change=${this._handleRowCheckboxClick}
                  .rowId=${e[this.id]}
                  .disabled=${!1===e.selectable}
                  .checked=${this._checkedRows.includes(String(e[this.id]))}
                >
                </ha-checkbox>
              </div>
            `:""}
        ${Object.entries(this.columns).map((([t,a])=>a.hidden?"":i.dy`
            <div
              role="cell"
              class="mdc-data-table__cell ${(0,o.$)({"mdc-data-table__cell--numeric":"numeric"===a.type,"mdc-data-table__cell--icon":"icon"===a.type,"mdc-data-table__cell--icon-button":"icon-button"===a.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===a.type,grows:Boolean(a.grows),forceLTR:Boolean(a.forceLTR)})}"
              style=${a.width?(0,c.V)({[a.grows?"minWidth":"width"]:a.width,maxWidth:a.maxWidth?a.maxWidth:""}):""}
            >
              ${a.template?a.template(e[t],e):e[t]}
            </div>
          `))}
      </div>
    `:i.dy``}},{kind:"method",key:"_sortFilterData",value:async function(){const e=(new Date).getTime();this.curRequest++;const t=this.curRequest;let r=this.data;this._filter&&(r=await this._memFilterData(this.data,this._sortColumns,this._filter));const i=this._sortColumn?(async(e,t,r,i)=>(b||(b=(0,_.Ud)(new Worker(new URL(a.p+a.u(7406),a.b)))),b.sortData(e,t,r,i)))(r,this._sortColumns[this._sortColumn],this._sortDirection,this._sortColumn):r,[l]=await Promise.all([i,u.y]),o=(new Date).getTime()-e;if(o<100&&await new Promise((e=>setTimeout(e,100-o))),this.curRequest===t){if(this.appendRow||this.hasFab){const e=[...l];this.appendRow&&e.push({append:!0,content:this.appendRow}),this.hasFab&&e.push({empty:!0}),this._items=e}else this._items=l;this._filteredData=l}}},{kind:"field",key:"_memFilterData",value:()=>(0,n.Z)((async(e,t,r)=>(async(e,t,r)=>(b||(b=(0,_.Ud)(new Worker(new URL(a.p+a.u(4813),a.b)))),b.filterData(e,t,r)))(e,t,r)))},{kind:"method",key:"_handleHeaderClick",value:function(e){const t=e.currentTarget.columnId;this.columns[t].sortable&&(this._sortDirection&&this._sortColumn===t?"asc"===this._sortDirection?this._sortDirection="desc":this._sortDirection=null:this._sortDirection="asc",this._sortColumn=null===this._sortDirection?void 0:t,(0,h.B)(this,"sorting-changed",{column:t,direction:this._sortDirection}))}},{kind:"method",key:"_handleHeaderRowCheckboxClick",value:function(e){e.target.checked?(this._checkedRows=this._filteredData.filter((e=>!1!==e.selectable)).map((e=>e[this.id])),this._checkedRowsChanged()):(this._checkedRows=[],this._checkedRowsChanged())}},{kind:"field",key:"_handleRowCheckboxClick",value(){return e=>{const t=e.currentTarget,a=t.rowId;if(t.checked){if(this._checkedRows.includes(a))return;this._checkedRows=[...this._checkedRows,a]}else this._checkedRows=this._checkedRows.filter((e=>e!==a));this._checkedRowsChanged()}}},{kind:"field",key:"_handleRowClick",value(){return e=>{const t=e.target;if(["HA-CHECKBOX","MWC-BUTTON"].includes(t.tagName))return;const a=e.currentTarget.rowId;(0,h.B)(this,"row-click",{id:a},{bubbles:!1})}}},{kind:"method",key:"_checkedRowsChanged",value:function(){this._items.length&&(this._items=[...this._items]),(0,h.B)(this,"selection-changed",{value:this._checkedRows})}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter||this._debounceSearch(e.detail.value)}},{kind:"method",key:"_calcTableHeight",value:async function(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}},{kind:"method",decorators:[(0,l.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"get",static:!0,key:"styles",value:function(){return[f.$c,i.iv`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          width: 100%;
          height: 52px;
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          width: 100%;
          border-bottom: 1px solid var(--divider-color);
          overflow-x: auto;
        }

        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          width: 60px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--checkbox,
        :host([dir="rtl"]) .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 0;
          /* @noflip */
          padding-right: 16px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
        }

        .mdc-data-table__cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: right;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--numeric {
          /* @noflip */
          text-align: left;
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          width: 54px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: right;
        }

        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: 8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-icon,
        :host([dir="rtl"])
          .mdc-data-table__cell--icon:first-child
          ha-state-icon,
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: auto;
          margin-right: 8px;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: auto;
          margin-left: -8px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child,
        :host([dir="rtl"])
          .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child {
          padding-left: 8px;
          padding-right: 16px;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__header-cell--icon-button:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--icon-button:last-child {
          padding-right: 8px;
          padding-left: 16px;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.375rem;
          font-weight: 500;
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell {
          /* @noflip */
          text-align: right;
        }

        .mdc-data-table__header-cell--numeric {
          text-align: right;
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric {
          /* @noflip */
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric.sortable:hover,
        :host([dir="rtl"])
          .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: right;
        }

        /* custom from here */

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell span {
          left: auto;
          right: 0px;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: left 0.2s ease;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell > * {
          transition: right 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          right: -20px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable:not(.not-sorted)
          span,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.not-sorted:hover
          span {
          left: auto;
          right: 24px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable:not(.not-sorted)
          ha-svg-icon,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable:hover.not-sorted
          ha-svg-icon {
          left: auto;
          right: 12px;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
        }
        search-input {
          display: block;
          flex: 1;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
          overflow: overlay !important;
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
        lit-virtualizer {
          contain: size layout !important;
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=9fdf181b.js.map