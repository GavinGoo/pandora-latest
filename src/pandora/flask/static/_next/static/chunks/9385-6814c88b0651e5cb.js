"use strict";
(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([[9385], {
    42508: function(e, t, r) {
        var i = r(92379);
        function s() {
            return (s = Object.assign ? Object.assign.bind() : function(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var r = arguments[t];
                    for (var i in r)
                        ({}).hasOwnProperty.call(r, i) && (e[i] = r[i])
                }
                return e
            }
            ).apply(null, arguments)
        }
        t.Z = e => i.createElement("svg", s({
            xmlns: "http://www.w3.org/2000/svg",
            width: 14,
            height: 14,
            fill: "none",
            viewBox: "0 0 14 14"
        }, e), i.createElement("path", {
            stroke: "currentColor",
            strokeWidth: 1.2,
            d: "m10.67 9.087 2.252-6.347c.367-1.033-.63-2.03-1.662-1.662L4.913 3.33A2.6 2.6 0 0 0 3.33 4.913L1.078 11.26c-.367 1.033.63 2.03 1.662 1.662l6.347-2.251a2.6 2.6 0 0 0 1.584-1.584Z",
            style: {
                stroke: "currentColor",
                strokeOpacity: 1
            }
        }), i.createElement("path", {
            stroke: "currentColor",
            d: "M7 8.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z",
            style: {
                stroke: "currentColor",
                strokeOpacity: 1
            }
        }))
    },
    39385: function(e, t, r) {
        r.d(t, {
            $: function() {
                return k
            },
            m: function() {
                return j
            }
        });
        var i = r(93951)
          , s = r(92745)
          , n = r(86025)
          , o = r(31438)
          , a = r(15913)
          , l = r(88667)
          , c = r(19841)
          , d = r(49764)
          , u = r(30478)
          , f = r(4160)
          , m = r(4858)
          , h = r(30853)
          , g = r(28146)
          , p = r(95033)
          , y = r(47762)
          , b = r(53114)
          , x = r(2118)
          , v = r(651);
        function j(e) {
            let {clientThreadId: t, onNewThread: r} = e
              , o = (0,
            s.XK)(t)
              , a = (0,
            i.t)()
              , {isUnauthenticated: l} = (0,
            n.u)()
              , c = (0,
            s.eV)(t)
              , d = (0,
            u.V_)();
            return l ? null : (0,
            v.jsxs)(v.Fragment, {
                children: [(0,
                v.jsx)(m.Y, {
                    onNewThread: r
                }), a?.canInteractWithGizmos() ? (0,
                v.jsx)(p.Dy, {
                    currentGizmoId: c
                }) : (0,
                v.jsx)(y.Z, {}), !l && (0,
                v.jsx)(f.Z, {
                    activeId: d ? void 0 : o,
                    isInPopover: !1
                })]
            })
        }
        function k(e) {
            let {className: t, onNewThread: r} = e
              , i = (0,
            d.Z)()
              , s = (0,
            a.w$)()
              , {value: n} = (0,
            l.sB)("1334159177");
            return (0,
            v.jsxs)("div", {
                className: (0,
                c.default)("flex justify-between", t),
                children: [(0,
                v.jsx)(h.u, {
                    sideOffset: 4,
                    label: i.formatMessage({
                        id: "e7SzX9",
                        defaultMessage: "Close sidebar"
                    }),
                    className: "flex",
                    side: "right",
                    children: (0,
                    v.jsx)(x.W, {
                        "aria-label": i.formatMessage({
                            id: "e7SzX9",
                            defaultMessage: "Close sidebar"
                        }),
                        onClick: () => {
                            s ? o.vm.toggleNavSidebar() : o.vm.togglePopoverNavSidebar()
                        }
                        ,
                        icon: s ? g.BSo : g.Oqj,
                        surfaceContext: "secondary"
                    })
                }), !n && (0,
                v.jsx)(b.y4, {
                    onClick: r
                })]
            })
        }
    },
    3483: function(e, t, r) {
        r.d(t, {
            V: function() {
                return g
            }
        });
        var i = r(98601)
          , s = r(83963)
          , n = r(24098)
          , o = r.n(n)
          , a = r(49764)
          , l = r(75325)
          , c = r(47584)
          , d = r(59144)
          , u = r(24434)
          , f = r(651);
        function m(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var i = Object.getOwnPropertySymbols(e);
                t && (i = i.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, i)
            }
            return r
        }
        function h(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? m(Object(r), !0).forEach(function(t) {
                    (0,
                    i.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : m(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function g(e) {
            let {title: t, handleDelete: r, onClose: i} = e
              , n = (0,
            a.Z)()
              , c = (0,
            s.ll)();
            return (0,
            f.jsxs)(u.Z, {
                isOpen: !0,
                onClose: i,
                type: "success",
                title: n.formatMessage(p.deleteModalTitle),
                primaryButton: (0,
                f.jsx)(d.Z.Button, {
                    title: n.formatMessage(p.deleteModalConfirm),
                    color: "danger",
                    onClick: () => {
                        r(),
                        i()
                    }
                }),
                secondaryButton: (0,
                f.jsx)(d.Z.Button, {
                    title: n.formatMessage(p.deleteModalCancel),
                    color: "secondary",
                    onClick: i
                }),
                children: [(0,
                f.jsx)(l.Z, h(h({}, p.deleteModalBody), {}, {
                    values: {
                        title: (0,
                        f.jsx)("strong", {
                            children: t
                        })
                    }
                })), c && (0,
                f.jsx)("div", {
                    className: "mt-2 text-sm text-token-text-tertiary",
                    children: (0,
                    f.jsx)(l.Z, {
                        id: "history.deleteModalMemoryDisclaimer",
                        defaultMessage: "To clear any memories from this chat, visit your <link>settings</link>.",
                        values: {
                            link: e => (0,
                            f.jsx)(o(), {
                                href: "#settings/Personalization",
                                shallow: !0,
                                className: "underline",
                                children: e
                            })
                        }
                    })
                })]
            })
        }
        let p = (0,
        c.vU)({
            deleteModalTitle: {
                id: "history.deleteModalTitle",
                defaultMessage: "Delete chat?"
            },
            deleteModalBody: {
                id: "history.deleteModalBody",
                defaultMessage: "This will delete {title}."
            },
            deleteModalConfirm: {
                id: "history.deleteModalConfirm",
                defaultMessage: "Delete"
            },
            deleteModalCancel: {
                id: "history.deleteModalCancel",
                defaultMessage: "Cancel"
            }
        })
    },
    4160: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return em
            }
        });
        var i = r(98601)
          , s = r(31438)
          , n = r(42420)
          , o = r(27393)
          , a = r(19841)
          , l = r(95638)
          , c = r(26430)
          , d = r(12654)
          , u = r(44043)
          , f = r(82187)
          , m = r(69262)
          , h = r(157)
          , g = r(21389)
          , p = r(88600)
          , y = r(92379)
          , b = r(47584)
          , x = r(49764)
          , v = r(75325)
          , j = r(15478)
          , k = r(17096)
          , w = r(11550)
          , M = r(39004)
          , C = r(2721)
          , O = r(53132)
          , S = r(92745)
          , N = r(86025)
          , P = r(43703)
          , T = r(13391)
          , E = r(15913)
          , D = r(3551)
          , Z = r(66290)
          , B = r(99976)
          , z = r(61619)
          , I = r(88667)
          , A = r(38482)
          , L = r.n(A)
          , G = r(24098)
          , R = r.n(G)
          , _ = r(15174)
          , K = r(651);
        function F(e) {
            let {text: t} = e
              , r = (0,
            _.Z)()
              , {0: i, 1: s} = (0,
            y.useState)(!0)
              , {0: n, 1: o} = (0,
            y.useState)(0)
              , a = (0,
            y.useMemo)( () => Array.from(t), [t])
              , l = (0,
            y.useMemo)( () => new $().humanTypingDelaysQuertyDistance(a), [a]);
            return (0,
            y.useEffect)( () => {
                t && i && (s(!0),
                l.forEach( (e, t) => {
                    setTimeout( () => {
                        r() && (o(t),
                        t === l.length - 1 && s(!1))
                    }
                    , e)
                }
                ))
            }
            , [l, r, i, t]),
            (0,
            K.jsx)(K.Fragment, {
                children: a.slice(0, n + 1).join("")
            })
        }
        class $ {
            qwertyDistance(e, t) {
                let r = {
                    q: [0, 0],
                    w: [1, 0],
                    e: [2, 0],
                    r: [3, 0],
                    t: [4, 0],
                    y: [5, 0],
                    u: [6, 0],
                    i: [7, 0],
                    o: [8, 0],
                    p: [9, 0],
                    a: [0, 1],
                    s: [1, 1],
                    d: [2, 1],
                    f: [3, 1],
                    g: [4, 1],
                    h: [5, 1],
                    j: [6, 1],
                    k: [7, 1],
                    l: [8, 1],
                    z: [0, 2],
                    x: [1, 2],
                    c: [2, 2],
                    v: [3, 2],
                    b: [4, 2],
                    n: [5, 2],
                    m: [6, 2]
                }
                  , [i,s] = r[e.toLowerCase()] ?? [0, 0]
                  , [n,o] = r[t.toLowerCase()] ?? [0, 0];
                return Math.abs(i - n) + Math.abs(s - o)
            }
            humanTypingDelaysQuertyDistance(e) {
                let t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 10
                  , r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : 100
                  , i = 0
                  , s = [];
                for (let n = 0; n < e.length; ++n) {
                    let o;
                    if (n > 0) {
                        let i = this.qwertyDistance(e[n - 1], e[n]);
                        o = 0 === i ? this.getRandomInt(t, Math.floor(r / 2)) : 1 === i ? this.getRandomInt(t, Math.floor(2 * r / 3)) : this.getRandomInt(t, r)
                    } else
                        o = this.getRandomInt(t, r);
                    s.push(o + i),
                    i += o
                }
                return s
            }
            getRandomInt(e, t) {
                return Math.floor(Math.random() * (t - e + 1)) + e
            }
        }
        var q = r(3483)
          , U = r(44395)
          , V = r(81522)
          , Y = r(30853)
          , W = r(28146)
          , H = r(24740)
          , Q = r(60682)
          , X = r(24241);
        let J = L()( () => Promise.all([r.e(6746), r.e(2245), r.e(1598)]).then(r.bind(r, 52245)).then(e => e.GizmoConversationOptionsDropdown), {
            loadableGenerated: {
                webpack: () => [52245]
            }
        });
        function ee(e) {
            let {conversation: t, conversationTitle: r, onOpenChange: i} = e
              , s = (0,
            x.Z)()
              , {isUnauthenticated: o} = (0,
            N.u)()
              , {eligible: a, markAsViewed: l} = (0,
            Q.qg)(Q.pm.ArchiveConversationOnboarding)
              , c = (0,
            S.ff)(t.id)
              , {0: d, 1: u} = (0,
            y.useState)(!1)
              , f = (0,
            n.NL)()
              , m = (0,
            Z.Z)();
            return ((0,
            y.useEffect)( () => (0,
            P.LW)(T.n, {
                deleteChat: e => {
                    let {serverThreadId: r} = e;
                    r === t.id && u(!0)
                }
                ,
                archiveChat: async e => {
                    let {serverThreadId: r} = e;
                    r === t.id && (await C.Z.patchConversation(t.id, {
                        is_archived: !0
                    }),
                    (0,
                    X.aM)(f),
                    I.m9.logEvent("chatgpt_conversation_archived"),
                    B.A.logEvent(z.M.conversationArchived),
                    a && (H.m.info(s.formatMessage({
                        defaultMessage: "You can view archived chats in Settings",
                        id: "HistoryGizmoItem.archiveChatOnboarding"
                    }), {
                        duration: 10,
                        hasCloseButton: !0
                    }),
                    l()),
                    c && m("/"))
                }
            }), [m, f, a, t.id, s, c, l]),
            o) ? null : (0,
            K.jsxs)(K.Fragment, {
                children: [(0,
                K.jsx)(Y.u, {
                    label: s.formatMessage({
                        id: "tJPHEQ",
                        defaultMessage: "Options"
                    }),
                    sideOffset: 4,
                    side: "top",
                    children: (0,
                    K.jsx)(J, {
                        clientThreadId: t.id,
                        onOpenChange: i,
                        children: (0,
                        K.jsx)("button", {
                            className: "flex items-center justify-center text-token-text-secondary transition hover:text-token-text-primary radix-state-open:text-token-text-secondary",
                            children: (0,
                            K.jsx)(W.nWS, {
                                className: "icon-md"
                            })
                        })
                    })
                }), d && (0,
                K.jsx)(q.V, {
                    title: r,
                    handleDelete: () => {
                        C.Z.patchConversation(t.id, {
                            is_visible: !1
                        }).then( () => {
                            (0,
                            X.aM)(f),
                            I.m9.logEvent("chatgpt_conversation_deleted"),
                            B.A.logEvent(z.M.conversationDeleted)
                        }
                        ),
                        c && m("/")
                    }
                    ,
                    onClose: () => {
                        u(!1)
                    }
                })]
            })
        }
        function et(e) {
            let {conversation: t, onClose: r} = e
              , {0: i, 1: s} = (0,
            y.useState)(t.title)
              , o = (0,
            n.NL)();
            function a() {
                i !== t.title && (S.tQ.setTitle(t.id, i, S._L.User),
                B.A.logEvent(z.M.renameThread, {
                    threadId: t.id,
                    content: i
                }),
                C.Z.patchConversation(t.id, {
                    title: i
                }).then( () => {
                    (0,
                    X.aM)(o)
                }
                ))
            }
            return (0,
            K.jsx)("input", {
                type: "text",
                value: i,
                onChange: e => {
                    s(e.target.value)
                }
                ,
                onKeyDown: e => {
                    switch (e.key) {
                    case "Escape":
                        r();
                        break;
                    case "Enter":
                        a(),
                        r()
                    }
                }
                ,
                onBlur: () => {
                    a(),
                    r()
                }
                ,
                autoFocus: !0,
                className: "w-full border border-token-border-light bg-transparent p-0 text-sm"
            })
        }
        function er(e) {
            let {conversation: t, isActive: r, elementRef: i, isPrimaryBackgroundColor: s} = e
              , n = (0,
            x.Z)()
              , {0: o, 1: l} = (0,
            y.useState)(!1)
              , {0: c, 1: d} = (0,
            y.useState)(!1)
              , u = O.p.useState(O.p.selectConversationStatus)(t.id)
              , f = O.p.useStore();
            (0,
            y.useEffect)( () => {
                if (2 === u && r) {
                    let e = setTimeout( () => {
                        f.setConversationStatus(t.id, null),
                        C.Z.clearConversationStatus(t.id)
                    }
                    , 500);
                    return () => clearTimeout(e)
                }
            }
            , [u, r, t.id, f]),
            (0,
            y.useEffect)( () => (0,
            P.LW)(T.n, {
                editTitle: e => {
                    let {serverThreadId: i} = e;
                    (i ? i === t.id : r) && l(!0)
                }
            }), [t.id, r]);
            let m = n.formatMessage({
                id: "mpXAeu",
                defaultMessage: "New chat"
            })
              , {resolvedTitle: h, isTypingEffect: g} = function(e, t, r) {
                let {title: i, titleSource: s} = (0,
                S.XL)(e)
                  , {0: n, 1: o} = (0,
                y.useState)(!1)
                  , a = i ?? t
                  , l = (0,
                y.useRef)(a);
                return (0,
                y.useEffect)( () => (r && s === S._L.Generated && a !== l.current && o(!0),
                () => {
                    l.current = a
                }
                ), [r, a, s]),
                {
                    isTypingEffect: n,
                    resolvedTitle: a
                }
            }(t.id, t.title, r)
              , p = (0,
            E.w$)()
              , b = g && r && p
              , {data: v} = (0,
            M.b9)(t.conversation_template_id ?? void 0)
              , j = (0,
            Z.Z)();
            return (0,
            K.jsxs)("div", {
                className: (0,
                a.default)("group relative rounded-lg active:opacity-90", r ? "bg-token-sidebar-surface-secondary" : "hover:bg-token-sidebar-surface-secondary", c && !r && "bg-token-sidebar-surface-secondary"),
                children: [(0,
                K.jsx)(R(), {
                    href: (0,
                    D.ZV)(t.id, v),
                    onClick: e => {
                        e.metaKey || e.ctrlKey || (e.preventDefault(),
                        r || function(e, t, r) {
                            let i = arguments.length > 3 && void 0 !== arguments[3] && arguments[3];
                            i || V.hx.abortAllRequests(),
                            B.A.logEvent(z.M.loadThread, {
                                threadId: t
                            }),
                            e((0,
                            D.ZV)(t, r))
                        }(j, t.id, v, I.m9.checkGate("3922476776")))
                    }
                    ,
                    onDoubleClick: () => {
                        l(!0)
                    }
                    ,
                    ref: i,
                    className: "flex items-center gap-2 p-2",
                    children: (0,
                    K.jsxs)("div", {
                        className: "relative grow overflow-hidden whitespace-nowrap",
                        dir: "auto",
                        children: [b ? (0,
                        K.jsx)(F, {
                            text: h || m
                        }) : h || m, (0,
                        K.jsx)("div", {
                            className: (0,
                            a.default)("absolute bottom-0 top-0 to-transparent ltr:right-0 ltr:bg-gradient-to-l rtl:left-0 rtl:bg-gradient-to-r", !!s && (r ? "from-token-sidebar-surface-secondary" : !r && c ? "from-token-sidebar-surface-secondary" : "from-token-main-surface-primary"), !s && (r ? "from-token-sidebar-surface-secondary" : !r && c ? "from-token-sidebar-surface-secondary" : "from-token-sidebar-surface-primary"), {
                                "from-token-main-surface-primary can-hover:group-hover:from-token-sidebar-surface-secondary": s && !r && !c,
                                "from-token-sidebar-surface-primary can-hover:group-hover:from-token-sidebar-surface-secondary": !s && !r && !c,
                                "w-10 from-60%": r || c,
                                "w-8 from-0% can-hover:group-hover:w-10 can-hover:group-hover:from-60%": !r && !c
                            })
                        })]
                    })
                }), o ? (0,
                K.jsx)("div", {
                    className: "absolute bottom-0 left-[7px] right-2 top-0 flex items-center bg-token-sidebar-surface-secondary",
                    children: (0,
                    K.jsx)(et, {
                        conversation: t,
                        onClose: () => {
                            l(!1)
                        }
                    })
                }) : r || 1 !== u ? r || 2 !== u ? (0,
                K.jsx)("div", {
                    className: (0,
                    a.default)("absolute bottom-0 top-0 items-center gap-1.5 pr-2 ltr:right-0 rtl:left-0", r || c ? "flex" : "hidden can-hover:group-hover:flex"),
                    children: (0,
                    K.jsx)(ee, {
                        conversation: t,
                        conversationTitle: h ?? t.title,
                        onOpenChange: e => {
                            d(e),
                            e && B.A.logEvent(z.M.conversationHistoryItemOpenMenu, {
                                conversationId: t.id
                            })
                        }
                    })
                }) : (0,
                K.jsx)("div", {
                    className: "absolute bottom-0 top-0 flex items-center gap-1.5 pr-2 ltr:right-0 rtl:left-0",
                    children: (0,
                    K.jsx)("div", {
                        className: "h-2 w-2 rounded-full bg-blue-selection"
                    })
                }) : (0,
                K.jsx)("div", {
                    className: "absolute bottom-0 top-0 flex items-center gap-1.5 pr-2 ltr:right-0 rtl:left-0",
                    children: (0,
                    K.jsx)(U.O, {
                        size: 18
                    })
                })]
            })
        }
        var ei = r(76608)
          , es = r(97537)
          , en = r(22591);
        function eo(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var i = Object.getOwnPropertySymbols(e);
                t && (i = i.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, i)
            }
            return r
        }
        function ea(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? eo(Object(r), !0).forEach(function(t) {
                    (0,
                    i.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : eo(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        let el = (0,
        b.vU)({
            historyBucketToday: {
                id: "history.bucket.today",
                defaultMessage: "Today"
            },
            historyBucketYesterday: {
                id: "history.bucket.yesterday",
                defaultMessage: "Yesterday"
            },
            historyBucketLastSeven: {
                id: "history.bucket.lastSeven",
                defaultMessage: "Previous 7 Days"
            },
            historyBucketLastThirty: {
                id: "history.bucket.lastThirty",
                defaultMessage: "Previous 30 Days"
            },
            unableToLoadHistory: {
                id: "history.unableToLoad",
                defaultMessage: "Unable to load history"
            },
            retryButton: {
                id: "history.retryButton",
                defaultMessage: "Retry"
            },
            showMoreButton: {
                id: "history.showMoreButton",
                defaultMessage: "Show more"
            }
        })
          , ec = {
            initial: e => {
                let {isNew: t} = e;
                return t ? {
                    opacity: 0,
                    height: 0,
                    overflow: "hidden"
                } : {}
            }
            ,
            animate: () => ({
                opacity: 1,
                height: "auto"
            }),
            exit: () => ({
                opacity: 0,
                height: 0
            })
        };
        function ed(e) {
            let {activeId: t, items: r, isPrimaryBackgroundColor: i, previousItems: n} = e
              , {isCollapsible: o, recentConversationLimit: l} = (0,
            en.j)()
              , c = r.slice(0, l);
            if (t) {
                let e = r.findIndex(e => e.id === t);
                e > l - 1 && c.push(r[e])
            }
            return (0,
            K.jsxs)(p.E.div, {
                className: (0,
                a.default)(i && "first:mt-0", "relative mt-5 first:mt-0 last:mb-5"),
                layout: "position",
                initial: {
                    height: "0",
                    opacity: 1,
                    position: "relative"
                },
                animate: {
                    height: "auto",
                    opacity: 1
                },
                transition: {
                    type: "spring",
                    stiffness: 225,
                    damping: 15,
                    mass: 1
                },
                children: [(0,
                K.jsx)(p.E.div, {
                    className: "sticky top-0 z-20",
                    layout: "position",
                    children: (0,
                    K.jsx)("span", {
                        className: "flex h-9 items-center",
                        children: (0,
                        K.jsx)(eg, {
                            children: (0,
                            K.jsx)(v.Z, {
                                id: "VbQeVG",
                                defaultMessage: "Recent"
                            })
                        })
                    })
                }), (0,
                K.jsx)("ol", {
                    children: c.map( (e, r) => {
                        let s = t === e.id
                          , o = n?.find(t => {
                            let {id: r} = t;
                            return r === e.id
                        }
                        );
                        return (0,
                        K.jsx)(eu, {
                            item: e,
                            isActive: s,
                            isFirstItem: 0 === r,
                            isExistingItem: !!o,
                            isPrimaryBackgroundColor: i
                        }, `history-item-${e.id}`)
                    }
                    )
                }), o && (0,
                K.jsx)(ei.x, {
                    type: "more",
                    onClick: s.vm.toggleHistoryCollapsed
                })]
            })
        }
        function eu(e) {
            let {elementRef: t, item: r, isActive: i, isFirstItem: s, isExistingItem: n, isPrimaryBackgroundColor: o} = e;
            return (0,
            K.jsx)(p.E.li, {
                className: (0,
                a.default)("relative", s ? "z-[15]" : ""),
                layout: "position",
                custom: {
                    isNew: !n
                },
                variants: ec,
                initial: "initial",
                animate: "animate",
                exit: "exit",
                children: (0,
                K.jsx)(er, {
                    isPrimaryBackgroundColor: o,
                    conversation: r,
                    isActive: i,
                    elementRef: t
                })
            })
        }
        function ef(e) {
            let {activeId: t, bucketedItems: r, items: i, hasNextPage: s, isPrimaryBackgroundColor: n, previousItems: o, infiniteScrollTriggerElementRef: l} = e;
            return (0,
            K.jsx)(K.Fragment, {
                children: [r.recent, r.dynamicMonths, r.dynamicYears].flatMap( (e, r) => (0,
                K.jsx)(y.Fragment, {
                    children: Object.entries(e).map( (e, c) => {
                        let[d,{items: u, label: f}] = e;
                        if ("today" !== d && !u.length)
                            return null;
                        let m = !!u.find(e => i.length > 0 && e.id === i[0]?.id);
                        return u.length > 0 && (0,
                        K.jsxs)("div", {
                            className: (0,
                            a.default)(n && "first:mt-0", "relative mt-5 first:mt-0 last:mb-5"),
                            children: [(0,
                            K.jsx)("div", {
                                className: "sticky top-0 z-20 bg-token-sidebar-surface-primary",
                                children: (0,
                                K.jsx)("span", {
                                    className: "flex h-9 items-center",
                                    children: (0,
                                    K.jsx)(eg, {
                                        children: f
                                    })
                                })
                            }), (0,
                            K.jsx)("ol", {
                                children: u.map( (e, r) => {
                                    let a = t === e.id
                                      , c = o?.find(t => {
                                        let {id: r} = t;
                                        return r === e.id
                                    }
                                    )
                                      , u = s && i[i.length - 5 - 1]?.id === e.id ? l : void 0;
                                    return (0,
                                    K.jsx)(eu, {
                                        item: e,
                                        isActive: a,
                                        isFirstItem: m && 0 === r,
                                        isExistingItem: !!c,
                                        isPrimaryBackgroundColor: n,
                                        elementRef: u
                                    }, `history-item-${e.id}-${d}`)
                                }
                                )
                            })]
                        }, `${d}-${r}-${c}`)
                    }
                    )
                }, `category-${r}`))
            })
        }
        var em = y.memo(function(e) {
            let {activeId: t, isPrimaryBackgroundColor: r, isInPopover: i} = e
              , a = (0,
            n.NL)()
              , p = (0,
            x.Z)()
              , {0: b, 1: j} = (0,
            y.useState)(!1)
              , {0: M, 1: C} = (0,
            y.useState)(0)
              , O = (0,
            k.Z)()
              , {conversations: S, hasNextPage: N, fetchNextPage: P, isLoading: T, isFetchingNextPage: E, isError: D} = (0,
            X.MO)()
              , Z = (0,
            y.useRef)(null)
              , B = (0,
            y.useCallback)(e => {
                T || null == e || (Z.current?.disconnect(),
                Z.current = new IntersectionObserver(e => {
                    e[0].isIntersecting && N && P()
                }
                ),
                Z.current.observe(e))
            }
            , [T, N, P]);
            (0,
            y.useEffect)( () => () => {
                Z.current?.disconnect()
            }
            , []);
            let z = function(e) {
                let t = (0,
                y.useRef)()
                  , r = (0,
                y.useRef)();
                return ((0,
                y.useEffect)( () => {
                    t.current = r.current,
                    r.current = e
                }
                , [e]),
                e === r.current) ? t.current : r.current
            }(S);
            (0,
            y.useEffect)( () => {
                O( () => {
                    C(M + 1)
                }
                , (0,
                c.Z)((0,
                d.Z)(), Date.now()) + 1e3)
            }
            , [M, O]);
            let I = 0 === S.length;
            (0,
            y.useEffect)( () => {
                I || o.Ef({
                    namespace: o.dG.ChatPageLoad
                })?.logTiming("render_history_items")
            }
            , [I]);
            let A = (0,
            y.useMemo)( () => S.reduce( (e, t) => {
                let r = new Date(t.update_time ?? t.create_time ?? 0)
                  , i = (0,
                l.Z)(new Date, r);
                if (0 === i)
                    e.recent.today.items.push(t);
                else if (i <= 1)
                    e.recent.yesterday.items.push(t);
                else if (i <= 7)
                    e.recent.lastSeven.items.push(t);
                else if (i <= 30)
                    e.recent.lastThirty.items.push(t);
                else if ((0,
                m.Z)(r)) {
                    let i = (0,
                    f.Z)(r)
                      , s = (0,
                    u.Z)(r)
                      , n = `${i}-${s}`;
                    e.dynamicMonths[n] ? e.dynamicMonths[n].items.push(t) : e.dynamicMonths[n] = {
                        label: p.formatDate(r, {
                            month: "long"
                        }),
                        items: [t]
                    }
                } else {
                    let i = (0,
                    f.Z)(r)
                      , s = `${i}-`;
                    e.dynamicYears[s] ? e.dynamicYears[s].items.push(t) : e.dynamicYears[s] = {
                        label: p.formatDate(r, {
                            year: "numeric"
                        }),
                        items: [t]
                    }
                }
                return e
            }
            , {
                recent: {
                    today: {
                        label: (0,
                        K.jsx)(v.Z, ea({}, el.historyBucketToday)),
                        items: []
                    },
                    yesterday: {
                        label: (0,
                        K.jsx)(v.Z, ea({}, el.historyBucketYesterday)),
                        items: []
                    },
                    lastSeven: {
                        label: (0,
                        K.jsx)(v.Z, ea({}, el.historyBucketLastSeven)),
                        items: []
                    },
                    lastThirty: {
                        label: (0,
                        K.jsx)(v.Z, ea({}, el.historyBucketLastThirty)),
                        items: []
                    }
                },
                dynamicMonths: {},
                dynamicYears: {}
            }), [M, S])
              , {isCollapsible: L} = (0,
            en.j)()
              , G = (0,
            s.tN)(e => e.isHistoryCollapsed);
            return (0,
            K.jsxs)(eh, {
                $centered: T || D || I,
                children: [I && T && (0,
                K.jsx)(es.Z, {
                    className: "m-auto"
                }), I && D && (0,
                K.jsxs)("div", {
                    className: "p-3 text-center italic text-token-text-tertiary",
                    children: [(0,
                    K.jsx)(v.Z, ea({}, el.unableToLoadHistory)), !b && (0,
                    K.jsx)("div", {
                        className: "mt-1",
                        children: (0,
                        K.jsx)(w.z, {
                            as: "button",
                            color: "primary",
                            size: "small",
                            className: "m-auto mt-2",
                            onClick: () => {
                                j(!0),
                                (0,
                                X.aM)(a)
                            }
                            ,
                            children: (0,
                            K.jsx)(v.Z, ea({}, el.retryButton))
                        })
                    })]
                }), !T && !I && (0,
                K.jsx)("div", {
                    children: (0,
                    K.jsx)(h.S, {
                        id: i ? "history-popover" : "history-sidebar",
                        children: (0,
                        K.jsx)(g.M, {
                            initial: !1,
                            children: L && G ? (0,
                            K.jsx)(ed, {
                                activeId: t,
                                items: S,
                                previousItems: z,
                                isPrimaryBackgroundColor: r
                            }) : (0,
                            K.jsx)(ef, {
                                activeId: t,
                                bucketedItems: A,
                                hasNextPage: N,
                                items: S,
                                previousItems: z,
                                isPrimaryBackgroundColor: r,
                                infiniteScrollTriggerElementRef: B
                            })
                        })
                    })
                }), E && (0,
                K.jsx)("div", {
                    className: "m-4 mb-5 flex justify-center",
                    children: (0,
                    K.jsx)(es.Z, {})
                })]
            })
        });
        let eh = j.Z.div`flex flex-col gap-2 pb-2 text-token-text-primary text-sm mt-5
${e => {
            let {$centered: t} = e;
            return t && "h-full justify-center items-center empty:hidden"
        }
        }`
          , eg = j.Z.h3`pb-2 pt-3 px-2 text-xs font-semibold text-ellipsis overflow-hidden break-all text-token-text-primary`
    },
    4858: function(e, t, r) {
        r.d(t, {
            Y: function() {
                return c
            }
        });
        var i = r(28086)
          , s = r(88667)
          , n = r(49764)
          , o = r(28146)
          , a = r(33162)
          , l = r(651);
        function c(e) {
            let {onNewThread: t} = e
              , r = (0,
            n.Z)()
              , {value: c} = (0,
            s.sB)("1334159177");
            return c ? (0,
            l.jsx)("div", {
                className: "mb-4",
                children: (0,
                l.jsx)(a.x, {
                    href: "/",
                    onClick: e => {
                        t ? (e.preventDefault(),
                        t()) : (0,
                        i.X)()
                    }
                    ,
                    hoverRightIcon: null,
                    icon: (0,
                    l.jsx)(o.bl$, {
                        className: "icon-lg text-token-text-secondary"
                    }),
                    isMenuOpen: !1,
                    label: r.formatMessage({
                        id: "mG13YW",
                        defaultMessage: "New chat"
                    }),
                    loggingGizmoId: "primary"
                })
            }) : null
        }
    },
    95033: function(e, t, r) {
        r.d(t, {
            Dy: function() {
                return U
            }
        });
        var i, s = r(98601), n = r(30853), o = r(12128), a = r(25899), l = r(39004), c = r(99555), d = r(10080), u = r(93951), f = r(86025), m = r(31438), h = r(3551), g = r(42420), p = r(58695), y = r(28146), b = r(66290), x = r(27393), v = r(88667), j = r(19841), k = r(88600), w = r(14015), M = r.n(w), C = r(38482), O = r.n(C), S = r(24098), N = r.n(S), P = r(92379), T = r(75325), E = r(49764), D = r(47584), Z = r(98095), B = r(34643), z = r(75372), I = r(15972), A = r(33162), L = r(47762), G = r(651);
        function R(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var i = Object.getOwnPropertySymbols(e);
                t && (i = i.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, i)
            }
            return r
        }
        function _(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? R(Object(r), !0).forEach(function(t) {
                    (0,
                    s.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : R(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        let K = O()( () => r.e(1793).then(r.bind(r, 61793)).then(e => e.GizmoKeepInSidebarMenuItem), {
            loadableGenerated: {
                webpack: () => [61793]
            }
        })
          , F = ((i = {})[i.Keep = 0] = "Keep",
        i[i.Recents = 1] = "Recents",
        i);
        function $(e) {
            let {isActive: t, isNewConversation: r} = e
              , i = (0,
            g.NL)()
              , s = (0,
            b.Z)();
            return [(0,
            G.jsx)("div", {
                className: "bg-token-sidebar-surface-primary pt-0",
                children: (0,
                G.jsx)(Y, {
                    gizmo: void 0,
                    isActive: t,
                    onClick: e => {
                        (0,
                        f.P)((0,
                        p.y_)(i)) && !r && (e.preventDefault(),
                        (0,
                        I.Xl)(s))
                    }
                })
            }),
            (0,G.jsx)
            ("div", {
                className: "bg-token-sidebar-surface-primary pt-0",
                children: (0,
                G.jsx)("div", {
                    tabindex: "1",
                    children: (0,
                G.jsx)("a", {
                    target: "_blank",
                    href: "https://github.com/GavinGoo/pandora-web/tree/dev",
                    className: "group flex h-10 items-center gap-2.5 rounded-lg bg-token-sidebar-surface-primary px-2 font-normal hover:bg-token-sidebar-surface-secondary",
                    children: [
                                (0,
                        G.jsx)("div", {
                            className: "h-6 w-6 flex-shrink-0",
                            children: (0,
                                G.jsx)("div", {
                                    className: "gizmo-shadow-stroke relative flex h-full items-center justify-center rounded-full bg-token-main-surface-primary text-token-text-primary",
                                    children: (0,
                                        G.jsx)("svg", {
                                            width: "24",
                                            height: "24",
                                            viewBox: "0 0 24 24",
                                            xmlns: "http://www.w3.org/2000/svg",
                                            className: t,
                                            children: [(0,
                                            G.jsx)("path", {
                                                d: "M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2Z",
                                                stroke: "currentColor"
                                            })]
                                        })
                                })
                        }),(0,
                        G.jsx)("div", {
                            className: "grow overflow-hidden text-ellipsis whitespace-nowrap text-sm text-token-text-primary",
                            children: "Star on GitHub :)"
                        })
                        
                    ]
                })
                })
            })
            
            ]
        }
        function q(e) {
            let {gizmo: t, currentGizmoId: r} = e
              , i = (0,
            P.useRef)(!1)
              , s = (0,
            m.tN)()
              , {0: n, 1: o} = (0,
            P.useState)(!1)
              , {itemsLeft: a, listItems: l, needsToCollapseItems: c} = function(e, t) {
                let r = M()(e, e => e.flair.kind)
                  , i = [...r[d.JK.FirstParty]?.map(e => {
                    let {resource: t} = e;
                    return {
                        gizmo: t,
                        section: F.Keep
                    }
                }
                ) ?? [], ...r[d.JK.SidebarKeep]?.map(e => {
                    let {resource: t} = e;
                    return {
                        gizmo: t,
                        section: F.Keep
                    }
                }
                ) ?? [], ...r[d.JK.Recent]?.slice(0, 2).map(e => {
                    let {resource: t} = e;
                    return {
                        gizmo: t,
                        section: F.Recents
                    }
                }
                ) ?? []]
                  , s = i.length > 5
                  , n = s && !t && i.length > 4 ? i.slice(0, 4) : i;
                return {
                    listItems: [...n.filter(e => {
                        let {section: t} = e;
                        return t === F.Keep
                    }
                    ), ...n.filter(e => {
                        let {section: t} = e;
                        return t === F.Recents
                    }
                    )],
                    itemsLeft: i.length - n.length,
                    needsToCollapseItems: s
                }
            }(t, n);
            return (0,
            P.useEffect)( () => {
                l.length > 0 && !i.current && (x.Ef({
                    namespace: x.dG.ChatPageLoad
                })?.logTiming("render_gizmo_sidebar"),
                i.current = !0)
            }
            , [l]),
            (0,
            G.jsxs)("div", {
                children: [l.map( (e, t) => {
                    let {gizmo: i, section: s} = e;
                    return (0,
                    G.jsxs)(P.Fragment, {
                        children: [t > 1 && s !== l[t - 1].section && (0,
                        G.jsx)("div", {
                            className: "my-2 ml-2 h-px w-7 bg-token-sidebar-surface-tertiary"
                        }), (0,
                        G.jsx)(Y, {
                            gizmo: i,
                            isActive: i.gizmo.id === r,
                            section: s
                        }, i.gizmo.id)]
                    }, t)
                }
                ), c ? (0,
                G.jsxs)("button", {
                    onClick: () => {
                        o(!n)
                    }
                    ,
                    className: "flex h-10 w-full items-center gap-2 rounded-lg px-2 text-sm text-token-text-primary hover:bg-token-sidebar-surface-secondary",
                    children: [(0,
                    G.jsx)("div", {
                        className: "flex h-6 w-6 flex-shrink-0 items-center justify-center",
                        children: (0,
                        G.jsx)(y.nWS, {
                            className: "icon-md text-token-text-primary"
                        })
                    }), (0,
                    G.jsx)("div", {
                        className: "flex grow items-center gap-1",
                        children: n ? (0,
                        G.jsxs)(G.Fragment, {
                            children: [(0,
                            G.jsx)(T.Z, {
                                id: "GizmoSidebarList.showLess",
                                defaultMessage: "See less"
                            }), (0,
                            G.jsx)(y.r0F, {
                                className: "icon-xs"
                            })]
                        }) : (0,
                        G.jsxs)(G.Fragment, {
                            children: [(0,
                            G.jsx)(T.Z, {
                                id: "GizmoSidebarList.showMoreItems",
                                defaultMessage: "{numMore} more",
                                values: {
                                    numMore: a
                                }
                            }), (0,
                            G.jsx)(y.Tg4, {
                                className: "icon-xs"
                            })]
                        })
                    })]
                }) : null, (0,
                G.jsx)(B.Z, {
                    children: (0,
                    G.jsx)(k.E.div, {
                        whileTap: {
                            scale: .98
                        },
                        children: (0,
                        G.jsx)(N(), {
                            href: (0,
                            h.cy)(),
                            onClick: () => {
                                "popover-nav" === s.activeSidebar && m.vm.setActiveSidebar(!1)
                            }
                            ,
                            children: (0,
                            G.jsx)(z.f, {
                                icon: y.frp,
                                children: (0,
                                G.jsx)(T.Z, _({}, W.exploreStoreEnabled))
                            })
                        }, "explore")
                    })
                })]
            })
        }
        function U(e) {
            let {currentGizmoId: t} = e
              , {data: {gizmos: r}={}} = (0,
            l.Wz)()
              , {value: i} = (0,
            v.sB)("1334159177");
            return (0,
            G.jsxs)(G.Fragment, {
                children: [!i && (0,
                G.jsx)($, {
                    isActive: void 0 === t,
                    isNewConversation: !0
                }), (0,
                G.jsx)(L.Z, {}), null != r ? (0,
                G.jsx)(q, {
                    gizmo: r,
                    currentGizmoId: t
                }) : null]
            })
        }
        function V(e) {
            let {gizmo: t, isOpen: r, setIsOpen: i, section: s} = e
              , n = (0,
            g.NL)();
            return (0,
            G.jsxs)(Z.d, {
                open: r,
                onOpenChange: i,
                triggerButton: (0,
                G.jsx)("button", {
                    className: (0,
                    j.default)("flex text-token-text-secondary hover:text-token-text-primary", r ? "" : "invisible group-hover:visible"),
                    children: (0,
                    G.jsx)(y.nWS, {
                        className: "icon-md"
                    })
                }),
                contentAlign: "start",
                sideOffset: 4,
                alignOffset: -4,
                size: "auto",
                children: [s === F.Recents && (0,
                G.jsx)(Z.Z.Item, {
                    onClick: async () => {
                        await c.U.updateGizmoSidebar(n, t.gizmo.id, "keep")
                    }
                    ,
                    children: (0,
                    G.jsx)(T.Z, _({}, W.keepInSidebar))
                }), (0,
                G.jsx)(K, {
                    gizmoResource: t
                })]
            })
        }
        function Y(e) {
            let t, {gizmo: r, historyDisabled: i, section: s, onClick: c} = e, f = (0,
            E.Z)(), {0: m, 1: h} = (0,
            P.useState)(!1), {0: g, 1: p} = (0,
            P.useState)(!1), b = (0,
            u.t)(), x = !!r?.gizmo.tags?.includes(d.U9.FirstParty);
            if (null != r)
                t = r.gizmo.display.name || a.zf;
            else {
                if (null == b)
                    return null;
                t = i ? f.formatMessage(W.clearChat) : b.canInteractWithGizmos() ? a.Dd : f.formatMessage({
                    id: "GizmoSidebarListItem.newChat",
                    defaultMessage: "New chat"
                })
            }
            return (0,
            G.jsx)(k.E.div, {
                whileTap: {
                    scale: .98
                },
                onMouseEnter: () => {
                    p(!0)
                }
                ,
                onMouseLeave: () => {
                    p(!1)
                }
                ,
                children: (0,
                G.jsx)(A.x, {
                    loggingGizmoId: r?.gizmo.id ?? "primary",
                    href: null != r ? (0,
                    l.m_)(r) : "/",
                    onClick: c,
                    icon: (0,
                    G.jsx)(o.Z, {
                        isFirstParty: null == r || x,
                        src: r?.gizmo.display.profile_picture_url,
                        className: "h-6 w-6 flex-shrink-0"
                    }),
                    isMenuOpen: m,
                    label: t,
                    hoverRightIcon: (0,
                    G.jsxs)("div", {
                        className: "flex gap-2",
                        children: [(g || m) && null != r && (0,
                        G.jsx)("div", {
                            className: "text-token-text-tertiary",
                            onClick: e => {
                                e.preventDefault()
                            }
                            ,
                            children: (0,
                            G.jsx)(V, {
                                gizmo: r,
                                isOpen: m,
                                setIsOpen: h,
                                section: s
                            })
                        }), (0,
                        G.jsx)(n.u, {
                            side: "right",
                            label: f.formatMessage(i ? W.clearChat : W.newChat),
                            className: "flex items-center",
                            children: (0,
                            G.jsx)("button", {
                                className: m ? "text-token-text-tertiary" : "invisible text-token-text-secondary hover:text-token-text-primary group-hover:visible",
                                children: i ? (0,
                                G.jsx)(y.Ezi, {
                                    className: "icon-md"
                                }) : (0,
                                G.jsx)(y.bl$, {
                                    className: "icon-md"
                                })
                            })
                        })]
                    })
                })
            })
        }
        let W = (0,
        D.vU)({
            exploreStoreEnabled: {
                id: "gizmo.exploreStoreEnabled",
                defaultMessage: "Explore GPTs"
            },
            keepInSidebar: {
                id: "gizmo.keepInSidebar",
                defaultMessage: "Keep in sidebar"
            },
            newChat: {
                id: "gizmo.newChat",
                defaultMessage: "New chat"
            },
            clearChat: {
                id: "gizmo.clearChat",
                defaultMessage: "Clear chat"
            }
        })
    },
    33162: function(e, t, r) {
        r.d(t, {
            x: function() {
                return c
            }
        });
        var i = r(99976)
          , s = r(61619)
          , n = r(19841)
          , o = r(24098)
          , a = r.n(o)
          , l = r(651);
        function c(e) {
            let {href: t, icon: r, label: o, hoverRightIcon: c, isMenuOpen: d, loggingGizmoId: u, onClick: f, target: m} = e;
            return (0,
            l.jsxs)(a(), {
                href: t,
                target: m,
                shallow: !0,
                className: (0,
                n.default)("group flex h-10 items-center gap-2.5 rounded-lg bg-token-sidebar-surface-primary px-2 font-normal", d ? "bg-token-main-surface-primary" : "hover:bg-token-sidebar-surface-secondary"),
                onClick: e => {
                    i.A.logNewChatButtonClicked({
                        location: "Sidebar gizmo list",
                        gizmo_id: u
                    }),
                    i.A.logEvent(s.M.sidebarClickGizmo, {
                        gizmo_id: u
                    }),
                    f?.(e)
                }
                ,
                children: [r, (0,
                l.jsx)("div", {
                    className: "grow overflow-hidden text-ellipsis whitespace-nowrap text-sm text-token-text-primary",
                    children: o
                }), c]
            })
        }
    },
    47762: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return j
            }
        });
        var i = r(28146)
          , s = r(60682)
          , n = r(98095)
          , o = r(33162)
          , a = r(40833)
          , l = r(34643)
          , c = r(31438)
          , d = r(15913)
          , u = r(19841)
          , f = r(88600)
          , m = r(92379)
          , h = r(75325)
          , g = r(42508)
          , p = r(651);
        function y() {
            let e = (0,
            s.qg)(s.pm.SonicSidebar)
              , {0: t, 1: r} = (0,
            m.useState)(!1);
            return e.isLoading || !e.eligible ? null : (0,
            p.jsx)(f.E.div, {
                className: "group pb-0",
                whileTap: {
                    scale: .98
                },
                children: (0,
                p.jsx)(b, {
                    children: (0,
                    p.jsx)(o.x, {
                        href: "/search",
                        target: "_blank",
                        icon: (0,
                        p.jsx)("div", {
                            className: (0,
                            u.default)("gizmo-shadow-stroke mr-[0.5] flex h-6 w-6 items-center justify-center rounded-full bg-token-main-surface-primary align-middle text-token-text-primary"),
                            children: (0,
                            p.jsx)(g.Z, {})
                        }),
                        label: "SearchGPT",
                        hoverRightIcon: (0,
                        p.jsxs)("div", {
                            className: "flex gap-3",
                            children: [(0,
                            p.jsx)(x, {
                                isOpen: t,
                                setIsOpen: r,
                                onDismiss: () => e.markAsViewed()
                            }), (0,
                            p.jsx)(i.Pfi, {
                                className: (0,
                                u.default)("icon-md text-token-text-tertiary", !t && "invisible group-hover:visible")
                            })]
                        }),
                        isMenuOpen: !1,
                        loggingGizmoId: "search-gpt-sidebar"
                    })
                })
            })
        }
        function b(e) {
            let {children: t} = e
              , r = function() {
                let e = (0,
                c.xH)()
                  , t = (0,
                s.qg)(s.pm.hasSeenSncSidebarTooltip)
                  , r = (0,
                l.c)()
                  , i = (0,
                c.ss)()
                  , {activeModals: n} = (0,
                c.tN)()
                  , o = (0,
                d.BL)();
                return !t.isLoading && t.eligible && !r && 0 === n.size && !e && !i && !o
            }()
              , i = (0,
            s.qg)(s.pm.hasSeenSncSidebarTooltip);
            return r ? (0,
            p.jsx)(a.v, {
                side: "right",
                show: !0,
                badge: "new",
                title: "Try SearchGPT",
                onDismiss: i.markAsViewed,
                sideOffset: 10,
                theme: "bright",
                description: "You're in. Get answers with real-time information from relevant sources, and ask follow-up questions.",
                children: (0,
                p.jsx)("div", {
                    className: "w-full",
                    children: t
                })
            }) : (0,
            p.jsx)(p.Fragment, {
                children: t
            })
        }
        function x(e) {
            let {isOpen: t, setIsOpen: r, onDismiss: s} = e;
            return (0,
            p.jsx)(n.d, {
                open: t,
                onOpenChange: r,
                triggerButton: (0,
                p.jsx)("button", {
                    className: (0,
                    u.default)("flex text-token-text-tertiary", t ? "" : "invisible group-hover:visible"),
                    onClick: e => {
                        e.preventDefault()
                    }
                    ,
                    children: (0,
                    p.jsx)(i.nWS, {
                        className: "icon-md"
                    })
                }),
                children: (0,
                p.jsx)(n.Z.Item, {
                    onClick: e => {
                        e.preventDefault(),
                        s()
                    }
                    ,
                    children: (0,
                    p.jsx)(h.Z, {
                        id: "sidebar.hideFromSidebar",
                        defaultMessage: "Hide from sidebar"
                    })
                })
            })
        }
        var v = r(88667);
        function j() {
            return (0,
            v.sB)("114024").value ? (0,
            p.jsx)(y, {}) : null
        }
    },
    34643: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return b
            },
            c: function() {
                return y
            }
        });
        var i = r(98601)
          , s = r(93951)
          , n = r(31438)
          , o = r(15913)
          , a = r(99976)
          , l = r(61619)
          , c = r(92379)
          , d = r(49764)
          , u = r(75325)
          , f = r(47584)
          , m = r(60682)
          , h = r(40833)
          , g = r(651);
        function p(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var i = Object.getOwnPropertySymbols(e);
                t && (i = i.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, i)
            }
            return r
        }
        function y() {
            let {activeModals: e} = (0,
            n.tN)()
              , t = (0,
            s.t)()
              , r = (0,
            m.qg)(m.pm.ExploreGPTs)
              , i = (0,
            m.qg)(m.pm.ExploreGPTsNewNux)
              , d = (0,
            n.ss)()
              , u = (0,
            n.xH)()
              , f = (0,
            o.BL)()
              , h = r.eligible && !r.isLoading && !u
              , g = i.eligible && !i.isLoading && !u && !d && !f;
            return e.size > 0 && (g = !1),
            !h && t?.hasPlusFeatures() && (g = !1),
            (0,
            c.useEffect)( () => {
                g && a.A.logEvent(l.M.storeDisplayNewNux)
            }
            , [g]),
            g
        }
        function b(e) {
            let {children: t} = e
              , r = y()
              , s = (0,
            d.Z)()
              , n = (0,
            m.qg)(m.pm.ExploreGPTsNewNux);
            return r ? (0,
            g.jsx)(h.v, {
                side: "right",
                show: !0,
                title: s.formatMessage(x.exploreGPTsTitle),
                onDismiss: n.markAsViewed,
                sideOffset: 20,
                theme: "bright",
                description: (0,
                g.jsx)(u.Z, function(e) {
                    for (var t = 1; t < arguments.length; t++) {
                        var r = null != arguments[t] ? arguments[t] : {};
                        t % 2 ? p(Object(r), !0).forEach(function(t) {
                            (0,
                            i.Z)(e, t, r[t])
                        }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : p(Object(r)).forEach(function(t) {
                            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                        })
                    }
                    return e
                }({}, x.exploreGPTsDescriptionNewNux)),
                children: t
            }) : (0,
            g.jsx)(g.Fragment, {
                children: t
            })
        }
        let x = (0,
        f.vU)({
            exploreGPTsTitle: {
                id: "gptExploreGPTs.title",
                defaultMessage: "Explore GPTs"
            },
            exploreGPTsDescription: {
                id: "gptExploreGPTs.description",
                defaultMessage: "Now you can discover GPTs created by the community"
            },
            exploreGPTsDescriptionNewNux: {
                id: "gptExploreGPTs.descriptionNewNux",
                defaultMessage: "Discover custom versions of ChatGPT created for specific use cases like writing, research, and coding."
            }
        })
    },
    13391: function(e, t, r) {
        r.d(t, {
            n: function() {
                return T
            },
            A3: function() {
                return N
            },
            yx: function() {
                return B
            },
            JS: function() {
                return Z
            }
        });
        var i, s = r(98601), n = r(15858), o = r(70879), a = r(99976), l = r(61619), c = r(79746), d = r(82363), u = r(91530), f = r.n(u), m = r(92379), h = r(47584), g = r(16757), p = r(24740), y = r(92745), b = r(31438), x = r(49763), v = r(22433), j = r(45248);
        let k = m.useLayoutEffect;
        function w(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var i = Object.getOwnPropertySymbols(e);
                t && (i = i.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, i)
            }
            return r
        }
        let M = /```.*?\n([\s\S]+?)\n?```[^`]*$/gms;
        var C = ((i = C || {}).Core = "Core",
        i.Chat = "Chat",
        i.Settings = "Settings",
        i);
        let O = function(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? w(Object(r), !0).forEach(function(t) {
                    (0,
                    s.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : w(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }({
            Mod: "mod",
            Comma: ","
        }, n.s)
          , S = {
            [O.Mod]: /Mac|iPod|iPhone|iPad/.test(window.navigator.platform) ? "⌘" : "Ctrl",
            [O.Comma]: ",",
            [O.Enter]: "⏎",
            [O.Escape]: "Esc",
            [O.ArrowUp]: "↑",
            [O.ArrowDown]: "↓",
            [O.ArrowLeft]: "←",
            [O.ArrowRight]: "→",
            [O.Backspace]: "⌫",
            [O.Delete]: "⌦",
            [O.Tab]: "⇥",
            [O.Control]: "Ctrl",
            [O.Shift]: "Shift"
        }
          , N = e => e.map(e => S[e] ?? e)
          , P = (0,
        h.vU)({
            newChat: {
                id: "keyboardActions.newChat",
                defaultMessage: "Open new chat"
            },
            focusPromptTextarea: {
                id: "keyboardActions.focusPromptTextarea",
                defaultMessage: "Focus chat input"
            },
            copyLastCodeBlock: {
                id: "keyboardActions.copyLastCodeBlock",
                defaultMessage: "Copy last code block"
            },
            copyLastResponse: {
                id: "keyboardActions.copyLastResponse",
                defaultMessage: "Copy last response"
            },
            toggleCustomInstructions: {
                id: "keyboardActions.toggleCustomInstructions",
                defaultMessage: "Set custom instructions"
            },
            navigationToggle: {
                id: "keyboardActions.navigationToggle",
                defaultMessage: "Toggle sidebar"
            },
            deleteChat: {
                id: "keyboardActions.deleteChat",
                defaultMessage: "Delete chat"
            },
            archiveChat: {
                id: "keyboardActions.archiveChat",
                defaultMessage: "Archive chat"
            },
            toggleKeyboardActions: {
                id: "keyboardActions.toggleKeyboardActions",
                defaultMessage: "Show shortcuts"
            }
        })
          , T = new x.V
          , E = e => {
            let {resetThreadAction: t, clientThreadId: r} = e;
            return [{
                key: "newChat",
                action: t || f(),
                actionMessageDescriptor: P.newChat,
                group: C.Core,
                keyboardBinding: [O.Mod, O.Shift, "o"],
                altKeyboardBindings: [[O.Mod, "k"]]
            }, {
                key: "focusPromptTextarea",
                action: o.go,
                actionMessageDescriptor: P.focusPromptTextarea,
                group: C.Chat,
                keyboardBinding: [O.Shift, O.Escape]
            }, {
                key: "copyLastCodeBlock",
                action: () => {
                    if (null != r) {
                        let e = y.tQ.getThreadCurrentLeafId(r)
                          , t = y.tQ.getThreadConversationTurns(r, e);
                        for (let e = t.length - 1; e >= 0; e--) {
                            let {messages: r} = t[e]
                              , i = [...r.reduce( (e, t) => null == t.err && t.message.author.role === g.uU.Assistant && "all" === t.message.recipient ? e + (e ? "\n\n" : "") + (0,
                            v.RR)(t.message) : e, "").matchAll(M)]
                              , s = i.length ? i[i.length - 1][1] : null;
                            if (null != s) {
                                (0,
                                c.v)(s).then( () => {
                                    p.m.success("Copied code block to clipboard")
                                }
                                );
                                break
                            }
                        }
                    }
                }
                ,
                actionMessageDescriptor: P.copyLastCodeBlock,
                group: C.Chat,
                keyboardBinding: [O.Mod, O.Shift, ";"],
                altKeyboardBindings: [[O.Mod, O.Shift, ":"]]
            }, {
                key: "copyLastResponse",
                action: () => {
                    null != r && y.tQ.copyLastMessageToClipboard(r, "keyboard").then( () => {
                        p.m.success("Last response copied to clipboard")
                    }
                    )
                }
                ,
                actionMessageDescriptor: P.copyLastResponse,
                group: C.Chat,
                keyboardBinding: [O.Mod, O.Shift, "c"]
            }, {
                key: "toggleCustomInstructions",
                action: () => b.vm.toggleModal(b.B.UserContext),
                actionMessageDescriptor: P.toggleCustomInstructions,
                group: C.Settings,
                keyboardBinding: [O.Mod, O.Shift, "i"]
            }, {
                key: "navigationToggle",
                action: () => b.vm.toggleNavSidebar(),
                actionMessageDescriptor: P.navigationToggle,
                group: C.Core,
                keyboardBinding: [O.Mod, O.Shift, "s"]
            }, {
                key: "deleteChat",
                action: () => {
                    if (r) {
                        let e = y.tQ.getServerThreadId(r);
                        e && T.publish({
                            kind: "deleteChat",
                            serverThreadId: e
                        })
                    }
                }
                ,
                actionMessageDescriptor: P.deleteChat,
                group: C.Chat,
                keyboardBinding: [O.Mod, O.Shift, O.Backspace],
                altKeyboardBindings: [[O.Mod, O.Shift, O.Delete]]
            }, {
                key: "toggleKeyboardActions",
                action: () => b.vm.toggleModal(b.B.KeyboardActions),
                actionMessageDescriptor: P.toggleKeyboardActions,
                group: C.Settings,
                keyboardBinding: [O.Mod, "/"]
            }]
        }
          , D = e => (function(e, t, r) {
            let i = e.map(e => {
                let {keyboardBinding: t} = e
                  , r = t.join("+");
                if (e.altKeyboardBindings) {
                    r = [r];
                    let t = e.altKeyboardBindings.map(e => e.join("+"));
                    r = r.concat(t)
                }
                return (0,
                j.ZP)(r, {
                    byKey: !0
                })
            }
            );
            k( () => {
                if (r?.enabled === !1)
                    return;
                let s = r => {
                    if (!r.repeat)
                        for (let s = 0; s < i.length; s++)
                            i[s](r) && (void 0 === e[s].enabled || e[s].enabled) && (r.preventDefault(),
                            t(e[s]),
                            e[s].action())
                }
                  , n = e => {
                    void 0 !== e.key && s(e)
                }
                  , o = document;
                return o.addEventListener("keydown", n),
                () => {
                    o.removeEventListener("keydown", n)
                }
            }
            , [e, r])
        }
        )(e, e => {
            a.A.logEvent(l.M.keyboardShortcut, {
                keyboardActionKey: e.key
            }),
            d.U.addAction("chatgpt_keyboard_shortcut", {
                keyboardActionKey: e.key
            })
        }
        , {
            enabled: !0
        })
          , Z = function() {
            let {resetThreadAction: e, clientThreadId: t} = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
            return (0,
            m.useMemo)( () => E({
                resetThreadAction: e,
                clientThreadId: t
            }).filter(e => {
                let {enabled: t=!0} = e;
                return t
            }
            ), [t, e])
        }
          , B = e => {
            let {resetThreadAction: t, clientThreadId: r} = e;
            D(Z({
                resetThreadAction: t,
                clientThreadId: r
            }))
        }
    },
    17096: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return s
            }
        });
        var i = r(92379);
        function s() {
            let e = (0,
            i.useRef)([])
              , t = (0,
            i.useRef)( (t, r) => {
                let i = setTimeout(t, r);
                return e.current.push(i),
                i
            }
            );
            return (0,
            i.useEffect)( () => {
                let t = e.current;
                return () => {
                    t.forEach(e => {
                        clearTimeout(e)
                    }
                    )
                }
            }
            , []),
            t.current
        }
    }
}]);
//# sourceMappingURL=9385-6814c88b0651e5cb.js.map
