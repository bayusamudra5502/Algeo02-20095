(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{39:function(e,a,t){},51:function(e,a,t){"use strict";t.r(a);var s=t(0),n=t.n(s),i=t(7),c=t.n(i),r=(t(39),t(3)),d=t.p+"static/media/pictures.f69c51c0.png",l=t(1);function j(e){var a=e.value,t=e.animated;return Object(l.jsx)("div",{className:"progress",children:Object(l.jsx)("div",{className:"progress-bar progress-bar-striped bg-proses-ok "+(t?"progress-bar-animated":""),style:{width:"".concat(100*a,"%"),height:"100%"}})})}var o=t(58),b=Object(s.createContext)();function u(e){var a=e.children,t=Object(s.useState)(!1),n=Object(r.a)(t,2),i=n[0],c=n[1];return Object(l.jsx)(b.Provider,{value:{isConnected:i,setConnect:c},children:a})}var m=b,h=Object(s.createContext)();function O(e){var a=e.children,t=Object(s.useState)({isCompressing:!1,progress:0}),n=Object(r.a)(t,2),i=n[0],c=n[1];return Object(l.jsx)(h.Provider,{value:{compressState:i,setCompressState:c},children:a})}var g=h,p=t(57),x=t(56),k=t.p+"static/media/plug.ca5edc1d.png";function v(){return Object(l.jsx)(p.a,{placement:"bottom",overlay:Object(l.jsx)(x.a,{id:"connect-tooltip",children:"Sambungkan Koneksi"}),children:Object(l.jsx)("button",{className:"connect-plug",children:Object(l.jsx)("img",{src:k,alt:"Connection Plug"})})})}function f(){var e=Object(s.useState)(!1),a=Object(r.a)(e,2),t=a[0],n=a[1],i=Object(s.useContext)(m).isConnected,c=Object(s.useContext)(g).compressState;return Object(l.jsxs)(l.Fragment,{children:[Object(l.jsxs)("div",{className:"title",children:[Object(l.jsx)("div",{className:"picture",children:Object(l.jsx)("img",{src:d,alt:"Gambar"})}),Object(l.jsxs)("div",{children:[Object(l.jsx)("h1",{className:"h2",children:"Image Compressor"}),Object(l.jsx)("p",{children:"Yuk buat ukuran file gambar lebih kecil"})]}),Object(l.jsxs)("div",{className:"status",children:[Object(l.jsx)("h2",{className:"sub-judul",children:"Status Koneksi"}),Object(l.jsxs)("div",{children:[Object(l.jsx)("span",{className:"statusbar "+(i?"connected":"disconnected")}),i?"Connected":"Disconnected",i?"":Object(l.jsx)(v,{})]})]}),c.isCompressing?Object(l.jsxs)("div",{children:[Object(l.jsx)("h2",{className:"sub-judul",children:"Proses Kompresi"}),Object(l.jsx)(j,{value:c.progress,animated:!0})]}):"",Object(l.jsxs)("div",{className:"bottom",children:[Object(l.jsx)("h2",{className:"sub-judul",children:"Tentang Program ini"}),Object(l.jsx)("p",{children:"Program ini dibuat oleh kelompok X"}),Object(l.jsxs)("p",{children:["Lihat informasi lengkap"," ",Object(l.jsx)("button",{class:"button-link",onClick:function(){return n(!0)},children:"disini"}),"."]})]})]}),Object(l.jsxs)(o.a,{show:t,centered:!0,onHide:function(){return n(!1)},children:[Object(l.jsx)(o.a.Header,{closeButton:!0,children:Object(l.jsx)(o.a.Title,{children:"Tentang Kami"})}),Object(l.jsxs)(o.a.Body,{children:[Object(l.jsxs)("div",{className:"header",children:[Object(l.jsx)("div",{className:"picture",children:Object(l.jsx)("img",{src:d,alt:"Gambar"})}),Object(l.jsx)("h1",{className:"h2 text-center my-2",children:"Image Compressor"}),Object(l.jsx)("p",{className:"h5 text-center text-muted",children:"Versi 1.0.0"})]}),Object(l.jsxs)("div",{className:"kontributor",children:[Object(l.jsx)("h2",{className:"sub-judul",children:"Kontributor"}),Object(l.jsxs)("ul",{children:[Object(l.jsx)("li",{children:"Firizky Ardiansyah (13520095)"}),Object(l.jsx)("li",{children:"Bayu Samudra (13520128)"}),Object(l.jsx)("li",{children:"Ikmal Alfaozi (13520125)"})]})]}),Object(l.jsxs)("div",{children:[Object(l.jsx)("h2",{className:"sub-judul",children:"Deskripsi Singkat"}),Object(l.jsx)("p",{children:"Kompresi gambar merupakan suatu tipe kompresi data yang dilakukan pada gambar digital. Dengan kompresi gambar, suatu file gambar digital dapat dikurangi ukuran filenya dengan baik tanpa mempengaruhi kualitas gambar secara signifikan. Terdapat berbagai metode dan algoritma yang digunakan untuk kompresi gambar pada zaman modern ini"}),Object(l.jsxs)("p",{children:[" ","Salah satu algoritma yang dapat digunakan untuk kompresi gambar adalah algoritma SVD (Singular Value Decomposition). Algoritma SVD didasarkan pada teorema dalam aljabar linier yang menyatakan bahwa sebuah matriks dua dimensi dapat dipecah menjadi hasil perkalian dari 3 sub-matriks yaitu matriks ortogonal U, matriks diagonal S, dan transpose dari matriks ortogonal V."," "]})]})]})]})]})}function N(){return Object(l.jsx)("main",{children:Object(l.jsx)(f,{})})}var C=function(){return Object(l.jsx)("div",{className:"App",children:Object(l.jsx)(N,{})})},S=function(e){e&&e instanceof Function&&t.e(3).then(t.bind(null,59)).then((function(a){var t=a.getCLS,s=a.getFID,n=a.getFCP,i=a.getLCP,c=a.getTTFB;t(e),s(e),n(e),i(e),c(e)}))};t(50);c.a.render(Object(l.jsx)(n.a.StrictMode,{children:Object(l.jsx)(u,{children:Object(l.jsx)(O,{children:Object(l.jsx)(C,{})})})}),document.getElementById("root")),S()}},[[51,1,2]]]);
//# sourceMappingURL=main.e06f6916.chunk.js.map