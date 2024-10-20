"use strict";
(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([[3127], {
    76608: function(e, t, r) {
        r.d(t, {
            x: function() {
                return l
            }
        });
        var n = r(19841)
          , a = r(75325)
          , i = r(28146)
          , s = r(651);
        function l(e) {
            let {type: t, onClick: r} = e
              , l = "more" === t ? i.eOB : i.BZB;
            return (0,
            s.jsx)("div", {
                className: (0,
                n.default)("group flex w-full items-center justify-start", "less" === t && "z-20", "more" === t && "mt-1"),
                children: (0,
                s.jsxs)("button", {
                    className: "flex flex-1 select-none items-center rounded-lg py-1 pl-4 text-sm tracking-tight hover:bg-token-sidebar-surface-secondary focus:ring-0",
                    onClick: r,
                    children: [(0,
                    s.jsx)(l, {
                        className: "icon-2xl -ml-3 mr-1 font-semibold text-token-text-secondary"
                    }), "more" === t ? (0,
                    s.jsx)(a.Z, {
                        id: "25xE8F",
                        defaultMessage: "See more"
                    }) : (0,
                    s.jsx)(a.Z, {
                        id: "1poXLj",
                        defaultMessage: "See less"
                    })]
                })
            })
        }
    },
    33127: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return w
            }
        });
        var n = r(71522)
          , a = r(86025)
          , i = r(19841)
          , s = r(92379)
          , l = r(31438)
          , o = r(15913)
          , c = r(51813)
          , d = r(66290)
          , u = r(88667)
          , m = r(75325)
          , f = r(98095)
          , p = r(28146)
          , g = r(15972)
          , h = r(91496)
          , x = r(28626)
          , b = r(30808)
          , v = r(75372)
          , j = r(651);
        let y = () => {
            let {openSettings: e} = (0,
            h.F)()
              , t = u.sB("3376455464")?.value
              , r = u.sB("90459671")?.value
              , n = (0,
            d.Z)();
            return (0,
            j.jsxs)("div", {
                className: "flex h-full flex-col gap-2 p-3",
                children: [(0,
                j.jsx)(v.f, {
                    icon: p.bl$,
                    onClick: () => {
                        (0,
                        g.Xl)(n),
                        l.vm.closeActiveSidebar()
                    }
                    ,
                    children: (0,
                    j.jsx)(m.Z, {
                        id: "0FupYP",
                        defaultMessage: "New chat"
                    })
                }), (0,
                j.jsx)("div", {
                    className: "flex grow items-center justify-center",
                    children: (0,
                    j.jsx)(x.LE, {})
                }), (0,
                j.jsxs)(f.d, {
                    contentClassName: "w-[298px]",
                    triggerButton: (0,
                    j.jsx)(v.f, {
                        icon: p.voc,
                        children: (0,
                        j.jsx)(m.Z, {
                            id: "y4Lkp7",
                            defaultMessage: "Settings and more"
                        })
                    }),
                    children: [(0,
                    j.jsx)(f.Z.Item, {
                        onClick: () => e(),
                        icon: p.SWE,
                        children: (0,
                        j.jsx)(m.Z, {
                            id: "HrRLkZ",
                            defaultMessage: "Settings"
                        })
                    }), t && r && (0,
                    j.jsx)(f.Z.Item, {
                        icon: p.U65,
                        onClick: () => {
                            l.vm.openModal(l.B.ReportConversation)
                        }
                        ,
                        children: (0,
                        j.jsx)(m.Z, {
                            id: "thread.report.0",
                            defaultMessage: "Report illegal content"
                        })
                    }), (0,
                    j.jsx)(f.Z.Separator, {}), (0,
                    j.jsx)(b.E, {})]
                })]
            })
        }
        ;
        function w(e) {
            let {children: t, hideNavigation: r=!1, mobileHeaderContent: d, mobileHeaderLeftContent: u, mobileHeaderRightContent: m, mobileHeaderBottomContent: f, sidebar: p, forceOpenDesktopSidebar: g=!1} = e
              , h = (0,
            o.w$)()
              , {isUnauthenticated: x} = (0,
            a.u)()
              , [b,v,M] = (0,
            l.tN)(e => [e.isDesktopNavCollapsed, e.activeStageSidebar, e.activeSidebar])
              , O = []
              , k = null;
            s.Children.forEach(t, e => {
                s.isValidElement(e) && (e.type === w.Sidebars ? k = e : O.push(e))
            }
            );
            let P = !x && !r && null != p
              , C = !r && !h && (P || x);
            return (0,
            j.jsxs)("div", {
                className: (0,
                i.default)("relative flex h-full w-full overflow-hidden transition-colors", "popover-nav" !== M && "z-0"),
                children: [P && (0,
                j.jsx)(n.ZP, {
                    children: (0,
                    j.jsx)(c.O_, {
                        isExpanded: g || !b,
                        isPopover: v || !h,
                        children: x ? (0,
                        j.jsx)(y, {}) : p
                    })
                }), (0,
                j.jsxs)("div", {
                    className: "relative flex h-full max-w-full flex-1 flex-col overflow-hidden",
                    children: [C && (0,
                    j.jsx)(n.ZP, {
                        children: (0,
                        j.jsx)(c.Vs, {
                            onClickOpenSidebar: () => l.vm.togglePopoverNavSidebar(),
                            showNavSidebar: P,
                            leftContent: u,
                            rightContent: m,
                            bottomContent: f,
                            children: d
                        })
                    }), (0,
                    j.jsx)("main", {
                        className: "relative h-full w-full flex-1 overflow-auto transition-width",
                        children: O
                    })]
                }), k]
            })
        }
        w.Sidebars = function(e) {
            let {children: t} = e;
            return (0,
            j.jsx)(j.Fragment, {
                children: t
            })
        }
    },
    51813: function(e, t, r) {
        r.d(t, {
            MP: function() {
                return C
            },
            Nz: function() {
                return S
            },
            O_: function() {
                return _
            },
            Vs: function() {
                return E
            },
            wb: function() {
                return N
            }
        });
        var n = r(98601)
          , a = r(52088)
          , i = r(11550)
          , s = r(28146)
          , l = r(16351)
          , o = r(69539)
          , c = r(86025)
          , d = r(82821)
          , u = r(66583)
          , m = r(99976)
          , f = r(19841)
          , p = r(88600)
          , g = r(34977)
          , h = r(92379)
          , x = r(75325)
          , b = r(47584)
          , v = r(31438);
        r(15913),
        r(30853);
        var j = r(53114)
          , y = r(90067)
          , w = r(56409)
          , M = r(651);
        let O = ["onClick", "className"];
        function k(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function P(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? k(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : k(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function C(e) {
            let {onClick: t, className: r} = e
              , n = (0,
            a.Z)(e, O);
            return (0,
            M.jsx)(y.zV, P({
                onClick: t,
                className: (0,
                f.default)(r, "flex-grow overflow-hidden")
            }, n))
        }
        function N(e) {
            let {onNewChatButtonClick: t} = e
              , {isUnauthenticated: r, isLoading: n} = (0,
            c.u)();
            return n || !r ? null : (0,
            M.jsx)(j.y4, {
                className: "mr-3",
                onClick: () => {
                    m.A.logNewChatButtonClicked({
                        location: "Mobile header"
                    }),
                    t()
                }
            })
        }
        function S(e) {
            let {clientThreadId: t, onNewChatButtonClick: r} = e
              , {isUnauthenticated: n, isLoading: a} = (0,
            c.u)()
              , i = (0,
            o.x)();
            return a ? null : n ? i ? (0,
            M.jsx)(Z, {}) : (0,
            M.jsx)(I, {}) : (0,
            M.jsxs)(M.Fragment, {
                children: [(0,
                M.jsx)(w.m2, {
                    conversationId: t
                }), (0,
                M.jsx)(j.y4, {
                    onClick: () => {
                        m.A.logNewChatButtonClicked({
                            location: "Mobile header"
                        }),
                        r()
                    }
                })]
            })
        }
        function I() {
            let e = (0,
            d.b)();
            return (0,
            M.jsx)(i.z, {
                as: "button",
                size: "small",
                color: "primary",
                onClick: () => {
                    let t = e({
                        authType: "signup"
                    });
                    m.A.logSignUpButtonClicked({
                        location: "Mobile Chat Stage Header",
                        provider: t
                    })
                }
                ,
                children: (0,
                M.jsx)(x.Z, P({}, A.signUpButtonText))
            })
        }
        function Z() {
            let e = (0,
            d.b)();
            return (0,
            M.jsx)(i.z, {
                as: "button",
                size: "small",
                color: "primary",
                onClick: () => {
                    let t = e({
                        authType: "login"
                    });
                    m.A.logLogInButtonClicked({
                        location: "Mobile Chat Stage Header",
                        provider: t
                    })
                }
                ,
                children: (0,
                M.jsx)(x.Z, P({}, l.kn.logInButtonText))
            })
        }
        function T(e) {
            let {onClick: t} = e;
            return (0,
            M.jsxs)("button", {
                type: "button",
                className: "inline-flex rounded-md hover:text-token-text-primary focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white active:opacity-50",
                onClick: t,
                children: [(0,
                M.jsx)("span", {
                    className: "sr-only",
                    children: (0,
                    M.jsx)(x.Z, P({}, A.openSidebar))
                }), (0,
                M.jsx)(s.Oqj, {
                    className: "icon-lg mx-2 text-token-text-secondary"
                })]
            })
        }
        let E = e => {
            let {onClickOpenSidebar: t, children: r, showNavSidebar: n, leftContent: a, rightContent: i, bottomContent: s} = e
              , l = (0,
            v.tN)(e => e.activeSidebar)
              , o = (0,
            g.useRouter)().asPath;
            return (0,
            h.useEffect)( () => {
                "popover-nav" === l && v.vm.setActiveSidebar(!1)
            }
            , [o]),
            (0,
            M.jsxs)(M.Fragment, {
                children: [(0,
                M.jsxs)("div", {
                    className: "sticky top-0 z-10 flex min-h-[60px] items-center justify-center border-transparent bg-token-main-surface-primary pl-0 md:hidden",
                    children: [(n || a) && (0,
                    M.jsxs)("div", {
                        className: "absolute bottom-0 left-0 top-0 ml-3 inline-flex items-center justify-center",
                        children: [n && (0,
                        M.jsx)(T, {
                            onClick: t
                        }), a]
                    }), r, i && (0,
                    M.jsx)("div", {
                        className: "absolute bottom-0 right-0 top-0 mr-3 inline-flex items-center justify-center",
                        children: i
                    })]
                }), s && (0,
                M.jsx)("div", {
                    className: "flex w-full items-center justify-center bg-token-main-surface-primary",
                    children: s
                })]
            })
        }
        ;
        function _(e) {
            let {isPopover: t=!1, isExpanded: r=!1, children: n} = e;
            return (0,
            M.jsxs)(M.Fragment, {
                children: [t && (0,
                M.jsx)(F, {
                    children: n
                }), (0,
                M.jsx)(D, {
                    isExpanded: !t && r,
                    children: n
                })]
            })
        }
        function D(e) {
            let {isExpanded: t, children: r} = e
              , n = (0,
            h.useRef)(null);
            return (0,
            M.jsx)(p.E.div, {
                className: "flex-shrink-0 overflow-x-hidden bg-token-sidebar-surface-primary",
                ref: n,
                initial: !1,
                animate: {
                    width: t ? "260px" : 0,
                    transition: {
                        duration: .165,
                        ease: "easeOut"
                    }
                },
                onAnimationStart: () => {
                    n.current && (n.current.style.visibility = "visible")
                }
                ,
                onAnimationComplete: () => {
                    n.current && (t || (n.current.style.visibility = "hidden"))
                }
                ,
                children: (0,
                M.jsx)("div", {
                    className: "h-full w-[260px]",
                    children: (0,
                    M.jsx)("div", {
                        className: "flex h-full min-h-0 flex-col",
                        children: r
                    })
                })
            })
        }
        function F(e) {
            let {children: t} = e
              , r = (0,
            v.tN)(e => e.activeSidebar);
            return (0,
            M.jsx)(u.fC, {
                open: "popover-nav" === r,
                onOpenChange: e => {
                    e || v.vm.setActiveSidebar(!1)
                }
                ,
                children: (0,
                M.jsxs)(u.h_, {
                    children: [(0,
                    M.jsx)(u.aV, {
                        className: "fixed inset-0 z-10 bg-white/50 radix-state-open:animate-show dark:bg-black/50"
                    }), (0,
                    M.jsx)(u.VY, {
                        className: "fixed left-0 top-0 z-50 h-full max-w-xs border-r border-gray-200 bg-token-sidebar-surface-primary shadow-[0_0_64px_0_rgba(0,0,0,0.07)] focus:outline-none radix-state-closed:animate-sidebarHide radix-state-open:animate-sidebarShow dark:border-gray-800",
                        children: t
                    })]
                })
            })
        }
        let A = (0,
        b.vU)({
            closeSidebar: {
                id: "navigation.closeSidebar",
                defaultMessage: "Close sidebar"
            },
            openSidebar: {
                id: "navigation.openSidebar",
                defaultMessage: "Open sidebar"
            },
            signUpButtonText: {
                id: "navigation.signUpButtonText",
                defaultMessage: "Sign up"
            }
        })
    },
    7331: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return z
            }
        });
        var n, a = r(98601), i = r(99333), s = r(55963), l = r(2721), o = r(60464), c = r(42420), d = r(56032), u = r(18939), m = r.n(u), f = r(92379), p = r(49764), g = r(75325), h = r(11550), x = r(19841), b = r(47584), v = r(75592), j = r(67526), y = r(30853), w = r(28146), M = r(651);
        function O(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function k(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? O(Object(r), !0).forEach(function(t) {
                    (0,
                    a.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : O(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function P(e) {
            return e.split(/[\s,]+/)
        }
        function C(e) {
            let {value: t, onChange: r, className: n} = e
              , a = (0,
            p.Z)()
              , {0: i, 1: s} = (0,
            f.useState)("")
              , l = (0,
            f.useCallback)(e => {
                if (i)
                    switch (e.key) {
                    case "Enter":
                    case ",":
                    case " ":
                        r([...t, ...P(i).map(N)]),
                        s(""),
                        e.preventDefault()
                    }
            }
            , [i, r, t]);
            return (0,
            M.jsx)(v.ZP, {
                className: (0,
                x.default)("react-select-container", n),
                isMulti: !0,
                onBlur: e => {
                    i && (r([...t, ...P(i).map(N)]),
                    s(i),
                    e.preventDefault())
                }
                ,
                classNamePrefix: "react-select",
                components: S,
                inputValue: i,
                isClearable: !0,
                menuIsOpen: !1,
                onChange: r,
                onInputChange: s,
                onKeyDown: l,
                placeholder: a.formatMessage(I.placeholder),
                value: t,
                "aria-labelledby": "add-emails-label",
                name: "add-member-emails"
            })
        }
        let N = e => ({
            label: e,
            value: e,
            isValid: o.F.test(e)
        })
          , S = {
            DropdownIndicator: () => null,
            IndicatorsContainer: () => null,
            ClearIndicator: () => null,
            MultiValueRemove: () => null,
            MultiValue: e => {
                let t = (0,
                p.Z)()
                  , r = (0,
                M.jsxs)("span", {
                    className: "flex items-center gap-1",
                    children: [(0,
                    M.jsx)("span", {
                        children: e.children
                    }), (0,
                    M.jsx)(w.tPq, {
                        className: "icon-sm"
                    })]
                })
                  , n = e.data.isValid ? r : (0,
                M.jsx)(y.u, {
                    label: t.formatMessage(I.tooltipInvalidEmail, {
                        email: e.data.value
                    }),
                    side: "top",
                    children: r
                });
                return (0,
                M.jsx)(j.c.MultiValue, k(k({}, e), {}, {
                    children: (0,
                    M.jsx)("button", {
                        className: (0,
                        x.default)("m-1 cursor-pointer rounded-full border border-transparent py-1 pl-3 pr-2 text-sm text-token-text-primary", e.data.isValid ? "bg-token-main-surface-secondary hover:border-token-border-medium hover:bg-token-main-surface-tertiary" : "bg-red-200 text-red-500"),
                        onClick: t => {
                            e.removeProps.onClick?.(t),
                            t.preventDefault()
                        }
                        ,
                        "aria-label": t.formatMessage(I.removeMember, {
                            member: e.data.value
                        }),
                        children: n
                    })
                }))
            }
        }
          , I = (0,
        b.vU)({
            membersAdded: {
                id: "emailsTextarea.membersAdded",
                defaultMessage: "+{count} {count, plural, one {member} other {members}}"
            },
            removeMember: {
                id: "emailsTextarea.removeMember",
                defaultMessage: "Remove {member}"
            },
            tooltipInvalidEmail: {
                id: "emailsTextarea.tooltipInvalidEmail",
                defaultMessage: '"{email}" may not be a valid email'
            },
            clearAllEntries: {
                id: "emailsTextarea.clearAllEntries",
                defaultMessage: "Clear all"
            },
            placeholder: {
                id: "emailsTextarea.placeholder",
                defaultMessage: "Type an email and press enter..."
            }
        });
        var Z = r(6440)
          , T = r(94668)
          , E = r(73062)
          , _ = r(36792)
          , D = r(24740)
          , F = r(12310)
          , A = r(44087);
        function L(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function B(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? L(Object(r), !0).forEach(function(t) {
                    (0,
                    a.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : L(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        let R = ((n = {})[n.INITIAL = 0] = "INITIAL",
        n[n.CSV_TABLE = 1] = "CSV_TABLE",
        n)
          , V = `email,role
user1@company.com,member
admin@company.com,admin
it@company.com,owner`
          , U = [];
        function z(e) {
            let {workspace: t, canResendInviteEmails: r, onCancel: n, cancelButtonText: a, onSuccess: u, fullWidthButtons: x=!1} = e
              , b = t.isOwnerOfAccount()
              , {0: v, 1: j} = (0,
            f.useState)(!1)
              , {0: y, 1: O} = (0,
            f.useState)(!1)
              , k = (0,
            f.useRef)(null)
              , P = t.isTeam()
              , N = (0,
            p.Z)()
              , {0: S, 1: I} = (0,
            f.useState)(!0)
              , {0: L, 1: z} = (0,
            f.useState)(!1)
              , {0: q, 1: G} = (0,
            f.useState)(R.INITIAL)
              , {0: $, 1: K} = (0,
            f.useState)([])
              , {0: X, 1: Q} = (0,
            f.useState)([])
              , {mutateAsync: Y} = function(e, t) {
                let r = (0,
                p.Z)()
                  , n = (0,
                c.NL)();
                return (0,
                d.D)({
                    mutationFn: async t => {
                        let {emails: n, role: a, resendEmails: i} = t
                          , s = []
                          , o = Math.max(5, Math.round(n.length / 10));
                        for (let e = 0; e < n.length; e += o)
                            s.push(n.slice(e, e + o));
                        let c = async t => l.Z.addWorkspaceUsers(e, t, a, i).then(e => (e.errored_emails.length > 0 && D.m.danger(r.formatMessage(H.inviteMessageFailure, {
                            emailsStr: e.errored_emails.map(e => {
                                let {email_address: t, error: r} = e;
                                return `${t}: ${r}`
                            }
                            ).join(", ")
                        })),
                        e.account_invites)).catch(e => {
                            throw D.m.danger(e.message),
                            e
                        }
                        );
                        return (await Promise.all(s.map(e => c(e)))).flat()
                    }
                    ,
                    onSuccess: () => {
                        n.invalidateQueries({
                            queryKey: ["workspace", "invites", e]
                        }),
                        t?.()
                    }
                })
            }(t.id, u)
              , J = (0,
            F.uo)()
              , ee = (0,
            F.VG)() ?? !0
              , {0: et, 1: er} = (0,
            f.useState)(U);
            (0,
            f.useEffect)( () => {
                if (!$?.length || !J?.length || ee) {
                    er(U);
                    return
                }
                let e = J.map(e => "@" + e.hostname.toLowerCase());
                er($.map(e => {
                    let {email: t} = e;
                    return t.toLowerCase()
                }
                ).filter(t => !e.some(e => t.endsWith(e))))
            }
            , [J, ee, $]);
            let en = W(b)
              , ea = async e => {
                let t = e.target.files?.[0];
                if (t) {
                    let e = await new Promise(e => {
                        if (t.size / 1048576 > 25)
                            e({
                                status: "error",
                                reason: "file_too_large"
                            });
                        else if ("text/csv" !== t.type)
                            e({
                                status: "error",
                                reason: "invalid_file_type"
                            });
                        else {
                            let r = new FileReader;
                            r.readAsText(t),
                            r.onload = function(t) {
                                let r = y
                                  , n = (t.target?.result).split("\n")
                                  , a = new Set;
                                e({
                                    status: "success",
                                    newRows: n.reduce( (e, t) => {
                                        let[n,i] = t.split(",").map(e => e.trim());
                                        return o.F.test(n) && !a.has(n) && (void 0 !== en[i] || r || (r = !0),
                                        e.push({
                                            email: n,
                                            role: en[i] ?? en.member
                                        })),
                                        a.add(n),
                                        e
                                    }
                                    , []),
                                    hasWarning: r
                                })
                            }
                        }
                    }
                    );
                    "success" === e.status ? (K(e.newRows),
                    G(R.CSV_TABLE),
                    O(e.hasWarning)) : "file_too_large" === e.reason ? D.m.danger(N.formatMessage(H.fileTooLargeWarning, {
                        maxSize: "25MB"
                    }), {
                        duration: 5
                    }) : "invalid_file_type" === e.reason && D.m.danger(N.formatMessage(H.fileIncorrectTypeWarning), {
                        duration: 5
                    })
                }
            }
              , ei = (e, t, r) => {
                let n = [...$];
                n[e] = B(B({}, n[e]), {}, {
                    [t]: r
                }),
                K(n)
            }
              , es = e => {
                K([...$.slice(0, e), ...$.slice(e + 1)])
            }
              , el = (0,
            f.useCallback)( () => {
                K([]),
                G(R.INITIAL),
                z(!1),
                Q([])
            }
            , [])
              , eo = async () => {
                z(!0);
                try {
                    $.length > 5 && D.m.info(N.formatMessage(H.inviteMessageLoading, {
                        numRows: $.length
                    }), {
                        hasCloseButton: !0
                    });
                    let e = [["admin", i.r3.ADMIN], ["owner", i.r3.OWNER], ["member", i.r3.STANDARD]]
                      , r = (await Promise.all(m()(e.map(e => {
                        let[t,r] = e
                          , n = $.filter(e => e.role === t).map(e => e.email);
                        return n.length > 0 && Y({
                            emails: n,
                            role: r,
                            resendEmails: S
                        })
                    }
                    )))).flat().length;
                    r > 0 && D.m.success(N.formatMessage(H.inviteSuccessToast, {
                        numRows: r,
                        userStr: 1 === r ? "user" : "users",
                        workspaceName: (0,
                        A.CV)(N, t)
                    })),
                    u?.(),
                    el()
                } finally {
                    z(!1)
                }
            }
              , ec = (0,
            M.jsx)(h.z, {
                color: "primary",
                size: x ? "large" : "medium",
                disabled: L || 0 === $.length || et.length > 0,
                onClick: eo,
                children: L ? N.formatMessage(H.inviteMemberInviteSubmitButtonLoading) : N.formatMessage(H.inviteMemberInviteSubmitButton)
            })
              , ed = (0,
            M.jsx)(h.z, {
                color: "primary",
                size: x ? "large" : "medium",
                disabled: 0 === X.length,
                onClick: () => {
                    let e = new Set;
                    K(X.reduce( (t, r) => (e.has(r.value) || t.push(r.value),
                    e.add(r.value),
                    t), []).map(e => ({
                        email: e,
                        role: en.member
                    }))),
                    G(R.CSV_TABLE)
                }
                ,
                children: N.formatMessage(H.inviteMemberInviteNextButton)
            });
            return (0,
            M.jsxs)("div", {
                className: "flex flex-col gap-2",
                children: [q === R.INITIAL && (0,
                M.jsxs)("div", {
                    className: "flex flex-col gap-3",
                    children: [(0,
                    M.jsxs)("div", {
                        className: "flex items-start justify-between gap-4",
                        children: [(0,
                        M.jsxs)("div", {
                            className: "flex flex-col gap-1",
                            children: [(0,
                            M.jsx)("label", {
                                htmlFor: "upload-csv",
                                id: "upload-csv-label",
                                children: (0,
                                M.jsx)(g.Z, B({}, H.importCSVLabel))
                            }), (0,
                            M.jsxs)("span", {
                                className: "text-sm text-token-text-tertiary",
                                children: [(0,
                                M.jsx)(g.Z, B(B({}, v ? H.helperCSVFormatHide : H.helperCSVFormatShow), {}, {
                                    values: {
                                        link: e => (0,
                                        M.jsx)("button", {
                                            className: "underline",
                                            onClick: () => {
                                                j(!v)
                                            }
                                            ,
                                            children: e
                                        })
                                    }
                                })), v && (0,
                                M.jsx)("pre", {
                                    className: "mt-4",
                                    children: V
                                })]
                            })]
                        }), (0,
                        M.jsx)("input", {
                            ref: k,
                            type: "file",
                            accept: ".csv,text/csv",
                            id: "upload-csv",
                            className: "hidden",
                            onChange: ea
                        }), (0,
                        M.jsx)(h.z, {
                            color: "secondary",
                            onClick: () => k.current?.click(),
                            children: (0,
                            M.jsx)(g.Z, B({}, H.importCSVButton))
                        })]
                    }), (0,
                    M.jsxs)("div", {
                        className: "flex flex-col gap-2",
                        children: [(0,
                        M.jsx)("label", {
                            htmlFor: "add-member-emails",
                            id: "add-emails-label",
                            children: (0,
                            M.jsx)(g.Z, B({}, H.addEmailsFieldName))
                        }), (0,
                        M.jsx)(C, {
                            value: X,
                            onChange: Q
                        })]
                    })]
                }), q === R.CSV_TABLE && (0,
                M.jsxs)(M.Fragment, {
                    children: [y && (0,
                    M.jsxs)("div", {
                        className: "flex w-full items-center bg-yellow-100 p-4",
                        children: [(0,
                        M.jsx)(w.ETw, {
                            className: "icon-sm mr-2 text-yellow-700"
                        }), (0,
                        M.jsx)("div", {
                            className: "flex-grow text-yellow-700",
                            children: (0,
                            M.jsx)(g.Z, B({}, H.unspecifiedRoleDescription))
                        })]
                    }), et.length > 0 && (0,
                    M.jsx)("div", {
                        className: "flex w-full items-center bg-red-100 p-4",
                        children: (0,
                        M.jsxs)("div", {
                            className: "flex-grow text-red-700",
                            children: [(0,
                            M.jsx)(g.Z, B({}, H.prohibitedExternalEmailDescription)), (0,
                            M.jsx)("pre", {
                                className: "my-1",
                                children: et.join(", ")
                            }), (0,
                            M.jsx)(g.Z, B({}, H.prohibitedExternalEmailResolution))]
                        })
                    }), (0,
                    M.jsxs)(_.Z.Root, {
                        size: "normal",
                        children: [(0,
                        M.jsxs)(_.Z.Header, {
                            children: [(0,
                            M.jsx)(_.Z.HeaderCell, {
                                children: (0,
                                M.jsx)(g.Z, B({}, H.inviteTableHeaderEmail))
                            }), (0,
                            M.jsx)(_.Z.HeaderCell, {
                                className: "pl-3 dark:bg-gray-900",
                                children: (0,
                                M.jsx)(g.Z, B({}, H.inviteTableHeaderRole))
                            }), (0,
                            M.jsx)(_.Z.HeaderCell, {})]
                        }), (0,
                        M.jsx)(_.Z.Body, {
                            children: $.map( (e, t) => (0,
                            M.jsxs)(_.Z.Row, {
                                children: [(0,
                                M.jsx)(_.Z.Cell, {
                                    children: (0,
                                    M.jsx)(Z.Z, {
                                        name: "email",
                                        type: "email",
                                        value: e.email,
                                        onChange: e => ei(t, "email", e.target.value),
                                        color: "neutral"
                                    })
                                }), (0,
                                M.jsx)(_.Z.Cell, {
                                    children: (0,
                                    M.jsxs)(E.Z.Root, {
                                        value: e.role,
                                        onValueChange: e => ei(t, "role", e),
                                        children: [(0,
                                        M.jsxs)(E.Z.Trigger, {
                                            children: [(0,
                                            M.jsx)(E.Z.Value, {}), (0,
                                            M.jsx)(E.Z.Icon, {})]
                                        }), (0,
                                        M.jsx)(E.Z.Portal, {
                                            children: (0,
                                            M.jsxs)(E.Z.Content, {
                                                className: "border border-token-main-surface-secondary",
                                                children: [(0,
                                                M.jsx)(E.Z.Item, {
                                                    value: en.member,
                                                    children: (0,
                                                    M.jsx)(g.Z, B({}, H.inviteRoleMember))
                                                }), en.admin && (0,
                                                M.jsx)(E.Z.Item, {
                                                    value: en.admin,
                                                    children: (0,
                                                    M.jsx)(g.Z, B({}, H.inviteRoleAdmin))
                                                }), en.owner && (0,
                                                M.jsx)(E.Z.Item, {
                                                    value: en.owner,
                                                    children: (0,
                                                    M.jsx)(g.Z, B({}, H.inviteRoleOwner))
                                                })]
                                            })
                                        })]
                                    })
                                }), (0,
                                M.jsx)(_.Z.Cell, {
                                    textAlign: "right",
                                    children: (0,
                                    M.jsx)(w.XHJ, {
                                        onClick: () => es(t),
                                        className: "icon-sm mr-2 cursor-pointer text-token-text-secondary"
                                    })
                                })]
                            }, t))
                        })]
                    })]
                }), r && I && (0,
                M.jsx)("div", {
                    className: "mt-2 flex items-center text-left text-token-text-secondary",
                    children: (0,
                    M.jsx)(s.Z, {
                        id: "resend-emails",
                        checked: S,
                        onChange: e => I(e.currentTarget.checked),
                        label: N.formatMessage(H.resendEmailsFieldName)
                    })
                }), q === R.INITIAL && P && (0,
                M.jsx)("div", {
                    className: "mb-4",
                    children: (0,
                    M.jsx)(T.Z, {
                        children: (0,
                        M.jsx)(g.Z, B({}, H.teamInviteModalNote))
                    })
                }), (0,
                M.jsxs)("div", {
                    className: "flex justify-end gap-2",
                    children: [(0,
                    M.jsx)(h.z, {
                        color: "secondary",
                        size: x ? "large" : "medium",
                        onClick: () => {
                            q !== R.INITIAL ? G(R.INITIAL) : (el(),
                            n())
                        }
                        ,
                        children: q === R.INITIAL ? a : N.formatMessage(H.inviteMemberInviteBackButton)
                    }), q === R.INITIAL ? ed : ec]
                })]
            })
        }
        let W = e => {
            let t = {
                member: "member"
            };
            return e && (t.admin = "admin",
            t.owner = "owner"),
            t
        }
          , H = {
            importCSVLabel: {
                id: "adminPage.importCSVLabel",
                defaultMessage: "Import from CSV",
                description: "Name of label for import from CSV button"
            },
            helperCSVFormatHide: {
                id: "adminPage.helperCSVFormat",
                defaultMessage: 'The file must include email and an optional role on each line. Roles can be "member", "admin", or "owner". <link>Hide Example</link>',
                description: "Instructions for formatting the import CSV, with a link to hide the example"
            },
            helperCSVFormatShow: {
                id: "adminPage.helperCSVFormat",
                defaultMessage: 'The file must include email and an optional role on each line. Roles can be "member", "admin", or "owner". <link>Show Example</link>',
                description: "Instructions for formatting the import CSV, with a link to show an example"
            },
            importCSVButton: {
                id: "adminPage.importCSVButton",
                defaultMessage: "Upload",
                description: "Name of upload from CSV button"
            },
            addEmailsFieldName: {
                id: "adminPage.addEmailsFieldName.0",
                defaultMessage: "Emails",
                description: "Name of input for adding emails to workspace"
            },
            unspecifiedRoleDescription: {
                id: "adminPage.unspecifiedRoleDescription",
                defaultMessage: "Roles that were unspecified have been changed to Member.",
                description: "Description text for defaulting invite roles to member"
            },
            prohibitedExternalEmailDescription: {
                id: "adminPage.prohibitedExternalEmailDescription",
                defaultMessage: "The following emails are not a part of your organization's verified domains:",
                description: "Description text for error message"
            },
            prohibitedExternalEmailResolution: {
                id: "adminPage.prohibitedExternalEmailResolution",
                defaultMessage: 'Either remove these emails, enable "Allow External Domain Invites" from your workspace settings, or verify these email domains.',
                description: "Description text for error message"
            },
            inviteTableHeaderEmail: {
                id: "adminPage.inviteTableHeaderEmail",
                defaultMessage: "Email",
                description: "Label for email column of invite table header"
            },
            inviteTableHeaderRole: {
                id: "adminPage.inviteTableHeaderRole",
                defaultMessage: "Role",
                description: "Label for role column of invite table header"
            },
            inviteRoleMember: {
                id: "adminPage.inviteRoleMember",
                defaultMessage: "Member",
                description: "Member role for workspace invite"
            },
            inviteRoleAdmin: {
                id: "adminPage.inviteRoleAdmin",
                defaultMessage: "Admin",
                description: "Admin role for workspace invite"
            },
            inviteRoleOwner: {
                id: "adminPage.inviteRoleOwner",
                defaultMessage: "Owner",
                description: "Owner role for workspace invite"
            },
            fileTooLargeWarning: {
                id: "adminPage",
                defaultMessage: "File is too large. Please upload a CSV file smaller than {maxSize}.",
                description: "Error when uploading a file that is too large"
            },
            fileIncorrectTypeWarning: {
                id: "adminPage",
                defaultMessage: "Please upload a CSV file.",
                description: "Error when uploading a file that is not a CSV"
            },
            resendEmailsFieldName: {
                id: "adminPage.resendEmailsFieldName",
                defaultMessage: "Resend emails for existing invites",
                description: "Name of checkbox input for resending emails to workspace"
            },
            teamInviteModalNote: {
                id: "adminPage.teamInviteModalNote",
                defaultMessage: "Users that accept invites will be included as additional seats on your next invoice.",
                description: "Note for team plan invites that additional seats will be charged"
            },
            inviteMessageLoading: {
                id: "adminPage.inviteMessageLoading",
                defaultMessage: "Sending out {numRows} invites, this may take a minute...",
                description: "Loading message when invites are being sent"
            },
            inviteSuccessToast: {
                id: "adminPage.inviteSuccessToast",
                defaultMessage: "Invited {numRows} {userStr} to {workspaceName}",
                description: "Message on successfully sending out invites"
            },
            inviteMemberInviteNextButton: {
                id: "adminPage.inviteMemberInviteNextButton",
                defaultMessage: "Next",
                description: "The title of the invite member modal next button"
            },
            inviteMemberInviteSubmitButton: {
                id: "adminPage.inviteMemberInviteSubmitButton",
                defaultMessage: "Send invites",
                description: "The title of the invite member modal submit button"
            },
            inviteMemberInviteSubmitButtonLoading: {
                id: "adminPage.inviteMemberInviteSubmitButtonLoading",
                defaultMessage: "Sending invites...",
                description: "Button label while inviting members"
            },
            inviteMemberInviteBackButton: {
                id: "adminPage.inviteMemberInviteBackButton",
                defaultMessage: "Back",
                description: "The title of the invite member modal back button"
            },
            inviteMessageFailure: {
                id: "adminPage.inviteMessageFailure",
                defaultMessage: "Unable to invite {emailsStr}",
                description: "Message that shows which emails were unsuccessful at being invited"
            }
        }
    },
    25805: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return h
            }
        });
        var n = r(98601)
          , a = r(31438)
          , i = r(91530)
          , s = r.n(i)
          , l = r(49764)
          , o = r(75325)
          , c = r(47584)
          , d = r(24434)
          , u = r(7331)
          , m = r(12310)
          , f = r(651);
        function p(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function g(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? p(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : p(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function h(e) {
            let {workspace: t} = e
              , r = (0,
            l.Z)()
              , n = (0,
            a.EV)(a.B.InviteUsersToWorkspace)
              , i = (0,
            m.VG)() ?? !0
              , c = m.uo()?.map(e => e.hostname);
            return (0,
            f.jsx)(d.Z, {
                size: "custom",
                className: "max-w-lg text-sm",
                isOpen: n,
                onClose: s(),
                type: "success",
                title: null != t.data.name ? r.formatMessage(x.inviteMemberModalTitle, {
                    workspaceName: t.data.name
                }) : r.formatMessage(x.inviteMemberModalTitleUntitledWorkspace),
                description: (0,
                f.jsxs)(f.Fragment, {
                    children: [(0,
                    f.jsx)("p", {
                        children: (0,
                        f.jsx)(o.Z, g({}, x.inviteMemberModalDescription))
                    }), !!c?.length && !i && (0,
                    f.jsxs)("p", {
                        className: "mt-2",
                        children: [(0,
                        f.jsx)(o.Z, g({}, x.prohibitExternalDomainsDescription)), "\xa0", (0,
                        f.jsx)("b", {
                            children: c.join(", ")
                        })]
                    })]
                }),
                children: (0,
                f.jsx)(u.Z, {
                    workspace: t,
                    canResendInviteEmails: !0,
                    onCancel: () => a.vm.closeModal(a.B.InviteUsersToWorkspace),
                    onSuccess: () => a.vm.closeModal(a.B.InviteUsersToWorkspace),
                    cancelButtonText: r.formatMessage(x.inviteMemberInviteCancelButton)
                })
            })
        }
        let x = (0,
        c.vU)({
            inviteMemberInviteCancelButton: {
                id: "adminPage.inviteMemberInviteCancelButton",
                defaultMessage: "Cancel"
            },
            inviteMemberModalTitle: {
                id: "adminPage.inviteMemberModalTitle",
                defaultMessage: "Invite members to the {workspaceName} workspace"
            },
            inviteMemberModalTitleUntitledWorkspace: {
                id: "adminPage.inviteMemberModalTitleUntitledWorkspace",
                defaultMessage: "Invite members to this workspace"
            },
            inviteMemberModalDescription: {
                id: "adminPage.inviteMemberModalDescription",
                defaultMessage: "This workspace is private, only select members and roles can use this workspace. This workspace is opted out of training."
            },
            prohibitExternalDomainsDescription: {
                id: "ky8nVd",
                defaultMessage: "Only users from the following emails can be added to this workspace:"
            },
            fileTooLargeWarning: {
                id: "adminPage",
                defaultMessage: "File is too large. Please upload a CSV file smaller than {maxSize}."
            }
        })
    },
    28626: function(e, t, r) {
        r.d(t, {
            LE: function() {
                return eg
            },
            ZP: function() {
                return ef
            }
        });
        var n = r(98601)
          , a = r(16351)
          , i = r(93951)
          , s = r(86025)
          , l = r(82821)
          , o = r(31438)
          , c = r(12598)
          , d = r(99976)
          , u = r(65012)
          , m = r(88667)
          , f = r(19841)
          , p = r(92379)
          , g = r(69539)
          , h = r(45120)
          , x = r(49764)
          , b = r(75325)
          , v = r(47584)
          , j = r(15478)
          , y = r(11550)
          , w = r(30478)
          , M = r(76608);
        r(30853);
        var O = r(28146)
          , k = r(91496)
          , P = r(22591)
          , C = r(83322)
          , N = r(25805)
          , S = r(71829)
          , I = r(2721)
          , Z = r(41987)
          , T = r(66290)
          , E = r(84760)
          , _ = r(61619)
          , D = r(97537)
          , F = r(87440)
          , A = r(68810);
        function L(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        let B = {
            showFreeTrialLoadingPayment: !1,
            showConfirmDismissFreeTrial: !1,
            didCloseFreeTrial: !1
        }
          , R = (0,
        A.Ue)()( () => (function(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? L(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : L(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        )({}, B));
        function V(e) {
            R.setState({
                showFreeTrialLoadingPayment: e
            })
        }
        var U = r(24740)
          , z = r(88600)
          , W = r(98302)
          , H = r(651);
        function q(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function G(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? q(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : q(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function $(e) {
            let {showFreeTrialLoadingPayment: t, handleGetPaymentLink: r} = e
              , n = (0,
            x.Z)()
              , {data: a, isLoading: i, isSuccess: s} = (0,
            E.a)({
                queryKey: ["claimedReferralInvite"],
                queryFn: () => I.Z.getClaimedReferralInvite(),
                refetchOnMount: !1,
                refetchOnWindowFocus: !1,
                refetchInterval: !1,
                refetchOnReconnect: !1
            })
              , l = a?.invite_code
              , {0: o, 1: c} = (0,
            p.useState)(!1);
            if ((0,
            p.useEffect)( () => {
                l && !o && s && (c(!0),
                m.m9.logEvent("chatgpt_referral_show_claimed_sidebar_menu_promo"),
                d.A.logEvent(_.M.chatgptReferralShowClaimedSidebartMenuPromo))
            }
            , [l, c, o, s]),
            !l || i || !s)
                return null;
            let u = l.invite_metadata.invite_data
              , g = u?.referral_trial_duration_months ? u?.referral_trial_duration_months > 1 ? n.formatMessage(X.monthsOfBenefit, {
                referralTrialDurationMonths: u?.referral_trial_duration_months
            }) : n.formatMessage(X.daysOfBenefit, {
                referralTrialDurationDays: u?.referral_trial_duration_days
            }) : null;
            return (0,
            H.jsx)(z.E.div, {
                className: (0,
                f.default)("relative", {
                    "cursor-progress opacity-50": t
                }),
                layout: "position",
                initial: {
                    y: -10,
                    opacity: 1
                },
                animate: {
                    y: 0,
                    opacity: 1,
                    transition: {
                        duration: .1,
                        ease: "easeIn"
                    }
                },
                children: (0,
                H.jsxs)(K, {
                    className: (0,
                    f.default)(t && "opacity-75"),
                    onClick: () => {
                        t || (V(!0),
                        r())
                    }
                    ,
                    children: [(0,
                    H.jsxs)("div", {
                        className: "flex w-full flex-row items-center justify-start gap-3",
                        children: [(0,
                        H.jsx)(W.E33, {
                            className: "icon-sm shrink-0"
                        }), (0,
                        H.jsx)(b.Z, G(G({}, X.freeTrialCta), {}, {
                            values: {
                                duration: g
                            }
                        }))]
                    }), !t && (0,
                    H.jsx)(O.tPq, {
                        onClick: e => {
                            e.stopPropagation(),
                            R.setState({
                                showConfirmDismissFreeTrial: !0
                            }),
                            R.setState({
                                didCloseFreeTrial: !0
                            })
                        }
                        ,
                        className: "icon-md shrink-0 rounded-full p-0.5 text-token-text-tertiary opacity-50 transition-colors duration-200 hover:bg-[#0077FF] hover:text-red-500 group-hover:opacity-100"
                    }), (0,
                    H.jsx)("span", {
                        className: "absolute top-11 h-0 w-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-[#0077FF] transition-colors duration-200 group-hover:border-t-[#0077FF]"
                    })]
                })
            })
        }
        let K = j.Z.a`group relative mb-1 rounded-md hover:[#0077FF] bg-[#0077FF] flex px-3 min-h-[44px] py-1 items-center gap-3 transition-colors duration-200 dark:text-white cursor-pointer text-sm`
          , X = (0,
        v.vU)({
            freeTrialCta: {
                id: "PaymentMenuItems.freeTrialCta",
                defaultMessage: "Get {duration}!"
            },
            monthsOfBenefit: {
                id: "FreeTrialMenuItem.monthsOfBenefit",
                defaultMessage: "{referralTrialDurationMonths, plural, one {one month free} other {# months free}}"
            },
            daysOfBenefit: {
                id: "FreeTrialMenuItem.daysOfBenefit",
                defaultMessage: "{referralTrialDurationDays, plural, one {one day free} other {# days free}}"
            }
        });
        var Q = r(90067);
        function Y(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function J(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? Y(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : Y(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function ee() {
            let e = (0,
            x.Z)()
              , t = (0,
            i.hz)()
              , r = (0,
            i.t)()
              , n = !r
              , a = r?.hasPaidSubscription() ?? !1
              , s = r?.hasClaimedFreeTrial() ?? !1
              , l = (0,
            p.useMemo)( () => r?.subscriptionAnalyticsParams, [r])
              , o = async () => {
                V(!0),
                d.A.logEvent(_.M.clickAccountPaymentCheckout, l);
                try {
                    let e = await I.Z.getCheckoutLink(t);
                    window.location.href = e.url
                } catch (t) {
                    U.m.warning(e.formatMessage(ea.paymentErrorWarning), {
                        hasCloseButton: !0
                    }),
                    V(!1)
                } finally {}
            }
              , c = R(e => e.didCloseFreeTrial)
              , u = R(e => e.showFreeTrialLoadingPayment)
              , f = !c && s
              , g = r?.wasPaidCustomer() ?? !1
              , h = r?.isWorkspaceAccount() ?? !1
              , b = r?.isPlus() ?? !1
              , v = (0,
            T.Z)()
              , {setShowReferralInviteModal: j} = (0,
            F.C)(e => ({
                setShowReferralInviteModal: e.setShowReferralInviteModal
            }))
              , y = (0,
            p.useCallback)( () => {
                m.m9.logEvent("chatgpt_referral_invite_sidebar_clicked"),
                d.A.logEvent(_.M.chatgptReferralInviteSidebarClicked, l),
                j(!0, () => {
                    d.A.logEvent(_.M.clickSidebarAccountPaymentMenuItem, l)
                }
                )
            }
            , [l, j])
              , w = r?.isTeam() ?? !1;
            return (0,
            H.jsxs)(H.Fragment, {
                children: [(t?.includes(Z.a3) || a) && (0,
                H.jsx)(en, {
                    analyticsParams: l,
                    handleReferralInvite: y
                }), !a && f && (0,
                H.jsx)($, {
                    showFreeTrialLoadingPayment: u,
                    handleGetPaymentLink: o
                }), w && (0,
                H.jsx)(er, {}), !n && !h && (0,
                H.jsx)(Q.Vq, {
                    onClick: f ? () => {
                        u || (V(!0),
                        o())
                    }
                    : () => {
                        d.A.logEvent(_.M.clickSidebarAccountPaymentMenuItem, l),
                        (0,
                        S.MG)(v, "Sidebar account payment menu item")
                    }
                    ,
                    className: "m-0 rounded-lg px-2",
                    children: (0,
                    H.jsx)("span", {
                        className: "flex w-full flex-row flex-wrap-reverse justify-between",
                        children: (0,
                        H.jsx)("div", {
                            className: "flex items-center gap-2",
                            children: (0,
                            H.jsx)(et, {
                                wasPaidCustomer: g,
                                showFreeTrialLoadingPayment: u,
                                hasPlusSubscription: b
                            })
                        })
                    })
                })]
            })
        }
        let et = e => {
            let {wasPaidCustomer: t, showFreeTrialLoadingPayment: r, hasPlusSubscription: n} = e;
            return r ? (0,
            H.jsx)(D.Z, {
                className: "icon-sm shrink-0"
            }) : (0,
            H.jsxs)(H.Fragment, {
                children: [(0,
                H.jsx)("span", {
                    className: "flex h-7 w-7 items-center justify-center rounded-full border border-token-border-light",
                    children: (0,
                    H.jsx)(O.xIk, {
                        className: "icon-sm shrink-0"
                    })
                }), (0,
                H.jsx)("div", {
                    className: "flex flex-col",
                    children: t ? (0,
                    H.jsx)(b.Z, J({}, ea.renewPlus)) : (0,
                    H.jsxs)(H.Fragment, {
                        children: [(0,
                        H.jsx)("span", {
                            children: n ? (0,
                            H.jsx)(b.Z, J({}, ea.createATeamWorkspace)) : (0,
                            H.jsx)(b.Z, J({}, ea.upgradePlan))
                        }), (0,
                        H.jsx)("span", {
                            className: "line-clamp-1 text-xs text-token-text-tertiary",
                            children: n ? (0,
                            H.jsx)(b.Z, J({}, ea.upgradeToTeamUpsell)) : (0,
                            H.jsx)(b.Z, J({}, ea.upgradeToPlusUpsell))
                        })]
                    })
                })]
            })
        }
          , er = () => {
            let e = (0,
            i.t)();
            return (0,
            H.jsxs)(H.Fragment, {
                children: [(0,
                H.jsx)(Q.Vq, {
                    onClick: () => {
                        o.vm.openModal(o.B.InviteUsersToWorkspace)
                    }
                    ,
                    className: "rounded-lg",
                    children: (0,
                    H.jsx)("span", {
                        className: "flex w-full flex-row flex-wrap-reverse justify-between",
                        children: (0,
                        H.jsxs)("span", {
                            className: "flex items-center gap-2",
                            children: [(0,
                            H.jsx)("span", {
                                className: "flex h-7 w-7 items-center justify-center rounded-full border border-token-border-light",
                                children: (0,
                                H.jsx)(O.pF9, {
                                    className: "icon-sm shrink-0"
                                })
                            }), (0,
                            H.jsx)(b.Z, J({}, ea.inviteMembers))]
                        })
                    })
                }), null != e ? (0,
                H.jsx)(N.Z, {
                    workspace: e
                }) : null]
            })
        }
          , en = e => {
            let {analyticsParams: t, handleReferralInvite: r} = e
              , n = (0,
            i.hz)()
              , a = n?.includes(Z.a3) ?? !1
              , s = (0,
            i.t)()
              , {data: l} = (0,
            E.a)({
                queryKey: ["referralInvites"],
                queryFn: () => I.Z.getEligibleReferralInvites(),
                enabled: a
            })
              , o = s && !s.isOrWasPaidCustomer() && !s.hasPlusFeatures()
              , c = l?.invites_remaining && l?.invites_remaining > 0
              , u = o && c
              , {0: f, 1: g} = (0,
            p.useState)(!1);
            return ((0,
            p.useEffect)( () => {
                u && !f && (g(!0),
                m.m9.logEvent("chatgpt_referral_show_sidebar_menu_item"),
                d.A.logEvent(_.M.chatgptReferralShowSidebarMenuItem, t))
            }
            , [u, g, f, t]),
            u) ? (0,
            H.jsx)(Q.Vq, {
                onClick: r,
                className: "rounded-lg",
                children: (0,
                H.jsx)("span", {
                    className: "flex w-full flex-row flex-wrap-reverse justify-between",
                    children: (0,
                    H.jsxs)("span", {
                        className: "flex items-center gap-2",
                        children: [(0,
                        H.jsx)("span", {
                            className: "flex h-7 w-7 items-center justify-center rounded-full border border-token-border-light",
                            children: (0,
                            H.jsx)(O.pF9, {
                                className: "icon-sm shrink-0"
                            })
                        }), (0,
                        H.jsx)(b.Z, J({}, ea.inviteReferral))]
                    })
                })
            }) : null
        }
          , ea = (0,
        v.vU)({
            upgradePlan: {
                id: "PaymentMenuItems.upgradePlan",
                defaultMessage: "Upgrade plan"
            },
            createATeamWorkspace: {
                id: "PaymentMenuItems.createATeamWorkspace",
                defaultMessage: "Add Team workspace"
            },
            upgradeToTeamUpsell: {
                id: "PaymentMenuItems.upgradeToTeamUpsell",
                defaultMessage: "Collaborate on a Team plan"
            },
            upgradeToPlusUpsell: {
                id: "PaymentMenuItems.upgradeToPlusUpsell.0",
                defaultMessage: "Get GPT-4, DALL\xb7E, and more"
            },
            renewPlus: {
                id: "PaymentMenuItems.renewPlus",
                defaultMessage: "Renew Plus"
            },
            inviteReferral: {
                id: "PaymentMenuItems.inviteReferral",
                defaultMessage: "Refer a friend"
            },
            inviteMembers: {
                id: "PaymentMenuItems.inviteMembers.0",
                defaultMessage: "Invite members"
            },
            paymentErrorWarning: {
                id: "PaymentMenuItems.paymentErrorWarning",
                defaultMessage: "The payments page encountered an error. Please try again. If the problem continues, please visit help.openai.com."
            }
        });
        var ei = r(15913)
          , es = r(42420)
          , el = r(56032);
        let eo = () => (0,
        E.a)({
            queryKey: ["userSurvey"],
            queryFn: async () => I.Z.getActiveUserSurvey()
        })
          , ec = () => {
            let e = (0,
            es.NL)();
            return (0,
            el.D)({
                mutationFn: async e => {
                    let {surveyId: t, reason: r} = e;
                    return I.Z.completeUserSurvey(t, r)
                }
                ,
                onSuccess: async () => {
                    e.invalidateQueries({
                        queryKey: ["userSurvey"]
                    })
                }
            })
        }
        ;
        function ed() {
            let e = (0,
            x.Z)()
              , t = (0,
            ei.w$)()
              , {0: r, 1: n} = (0,
            p.useState)(!1)
              , a = eo().data?.survey
              , i = ec()
              , s = e => {
                n(!0),
                null != a && i.mutate({
                    surveyId: a.id,
                    reason: e
                })
            }
            ;
            return r || null == a ? null : (0,
            H.jsx)("div", {
                className: "mx-1 mb-1 rounded-sm bg-brand-blue-800",
                children: (0,
                H.jsxs)("div", {
                    className: "flex flex-col items-center justify-stretch gap-3 p-3 text-sm text-white",
                    children: [(0,
                    H.jsxs)("div", {
                        className: "flex w-full items-start",
                        children: [(0,
                        H.jsxs)("div", {
                            className: "flex flex-grow flex-col gap-1",
                            children: [(0,
                            H.jsx)("div", {
                                className: "font-bold",
                                children: (0,
                                H.jsx)(b.Z, {
                                    id: "navigation.survey.title",
                                    defaultMessage: "We are asking a small group of people for their opinion"
                                })
                            }), (0,
                            H.jsx)("div", {
                                children: (0,
                                H.jsx)(b.Z, {
                                    id: "navigation.survey.description",
                                    defaultMessage: "Could you spare few minutes to take a short survey?"
                                })
                            })]
                        }), (0,
                        H.jsx)("button", {
                            className: "text-white/25 hover:text-white/40",
                            onClick: () => s("dismissed"),
                            "aria-label": e.formatMessage({
                                id: "navigation.survey.dismiss",
                                defaultMessage: "Dismiss survey"
                            }),
                            children: (0,
                            H.jsx)(O.tPq, {
                                width: t ? "20px" : "24px",
                                height: t ? "20px" : "24px"
                            })
                        })]
                    }), (0,
                    H.jsxs)("a", {
                        href: a.link,
                        target: "_blank",
                        className: "flex w-full flex-row items-center justify-center gap-2 rounded bg-white/25 p-2 hover:bg-white/40",
                        rel: "noreferrer",
                        onClick: () => s("link_clicked"),
                        children: [(0,
                        H.jsx)(O.Pfi, {
                            className: "icon-sm"
                        }), (0,
                        H.jsx)(b.Z, {
                            id: "navigation.survey.takeSurvey",
                            defaultMessage: "Take survey"
                        })]
                    })]
                })
            })
        }
        function eu(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function em(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? eu(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : eu(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        function ef(e) {
            let {navHeader: t, children: r, className: n} = e
              , a = (0,
            x.Z)()
              , i = (0,
            p.useRef)(null)
              , l = (0,
            w.V_)()
              , {openSettings: d} = (0,
            k.F)()
              , {isUnauthenticated: u} = (0,
            s.u)()
              , {layer: m} = (0,
            h.AH)("1578749296")
              , g = m.get("is_sticky_toggle_off", !1);
            return (0,
            p.useEffect)( () => {
                g && o.vm.openSidebar()
            }
            , [g]),
            (0,
            p.useEffect)( () => {
                w._P.getModifiedSettings() && d()
            }
            , []),
            (0,
            H.jsx)(H.Fragment, {
                children: (0,
                H.jsxs)("div", {
                    className: "relative h-full w-full flex-1 items-start border-white/20",
                    children: [(0,
                    H.jsx)(c.f, {
                        asChild: !0,
                        children: (0,
                        H.jsx)("h2", {
                            children: (0,
                            H.jsx)(b.Z, em({}, ex.chatHistoryLabel))
                        })
                    }), (0,
                    H.jsxs)("nav", {
                        className: (0,
                        f.default)("flex h-full w-full flex-col px-3", n),
                        "aria-label": a.formatMessage(ex.chatHistoryLabel),
                        children: [t, (0,
                        H.jsx)(eh, {
                            ref: i,
                            $disableScroll: l && !u,
                            children: r
                        }), (0,
                        H.jsx)(ep, {})]
                    })]
                })
            })
        }
        function ep() {
            let {0: e} = (0,
            p.useState)( () => {
                let e = u.bX.getCookie(u.cn.Workspace);
                return "string" == typeof e && e !== a.bC
            }
            )
              , t = (0,
            i.t)()
              , r = t?.data == null
              , {isUnauthenticated: n} = (0,
            s.u)()
              , {openSettings: l} = (0,
            k.F)()
              , {isCollapsible: c} = (0,
            P.j)()
              , d = (0,
            o.tN)(e => e.isHistoryCollapsed);
            return e && r || !t ? null : n ? (0,
            H.jsx)(eg, {}) : (0,
            H.jsxs)("div", {
                className: (0,
                f.default)("flex flex-col py-2 empty:hidden dark:border-white/20", c && "-mx-3 border-t border-token-border-sharp px-3"),
                children: [c && !d && (0,
                H.jsx)(M.x, {
                    type: "less",
                    onClick: o.vm.toggleHistoryCollapsed
                }), (0,
                H.jsx)("div", {
                    className: "flex w-full items-center md:hidden",
                    children: (0,
                    H.jsx)("div", {
                        className: "max-w-[100%] grow",
                        children: (0,
                        H.jsx)(C.W, {
                            onClickSettings: () => l()
                        })
                    })
                })]
            })
        }
        let eg = () => {
            let e = (0,
            g.x)()
              , t = (0,
            l.b)()
              , r = (0,
            H.jsx)(y.z, {
                as: "button",
                size: "medium",
                color: e ? "secondary" : "primary",
                "data-testid": "signup-button",
                onClick: () => {
                    let e = t({
                        authType: "signup"
                    });
                    d.A.logSignUpButtonClicked({
                        location: "Sidebar bottom unit",
                        provider: e
                    }),
                    m.m9.logEvent("chatgpt_sidebar_signup_button_clicked")
                }
                ,
                children: (0,
                H.jsx)(b.Z, em({}, ex.unauthSignupCta))
            })
              , n = (0,
            H.jsx)(y.z, {
                as: "button",
                size: "medium",
                color: e ? "primary" : "secondary",
                "data-testid": "login-button",
                onClick: () => {
                    let e = t({
                        authType: "login"
                    });
                    d.A.logLogInButtonClicked({
                        location: "Sidebar bottom unit",
                        provider: e
                    }),
                    m.m9.logEvent("chatgpt_sidebar_login_button_clicked")
                }
                ,
                children: (0,
                H.jsx)(b.Z, em({}, ex.unauthLoginCta))
            });
            return (0,
            H.jsxs)("div", {
                className: "p-2",
                children: [(0,
                H.jsxs)("div", {
                    className: "mb-4 mt-2",
                    children: [(0,
                    H.jsx)("p", {
                        className: "mb-1 text-sm font-semibold text-token-text-primary",
                        children: (0,
                        H.jsx)(b.Z, em({}, e ? ex.logInOrSignUp : ex.signUpOrLogIn))
                    }), (0,
                    H.jsx)("p", {
                        className: "text-sm text-token-text-secondary",
                        children: (0,
                        H.jsx)(b.Z, {
                            id: "4qlPtW",
                            defaultMessage: "Get smarter responses, upload files and images, and more."
                        })
                    })]
                }), (0,
                H.jsx)("div", {
                    className: "flex flex-row items-start gap-2",
                    children: e ? [n, r] : [r, n]
                })]
            })
        }
          , eh = j.Z.div`flex-col flex-1 transition-opacity duration-500 relative -mr-2 pr-2
  ${e => {
            let {$disableScroll: t} = e;
            return t ? "overflow-y-hidden opacity-20 pointer-events-none" : "overflow-y-auto"
        }
        }`
          , ex = (0,
        v.vU)({
            chatHistoryLabel: {
                id: "NavigationContent.chatHistoryLabel",
                defaultMessage: "Chat history"
            },
            closeSidebar: {
                id: "NavigationContent.closeSidebar",
                defaultMessage: "Close sidebar"
            },
            signInToChat: {
                id: "NavigationContent.signInToChat",
                defaultMessage: "Sign in to ChatGPT"
            },
            signUpOrLogIn: {
                id: "NavigationContent.signUpOrLogIn",
                defaultMessage: "Sign up or log in"
            },
            logInOrSignUp: {
                id: "NavigationContent.logInOrSignUp",
                defaultMessage: "Log in or sign up"
            },
            unauthSignupCta: {
                id: "NavigationContent.unauthSignupCta",
                defaultMessage: "Sign up"
            },
            unauthLoginCta: {
                id: "NavigationContent.unauthLoginCta",
                defaultMessage: "Log in"
            }
        })
    },
    75372: function(e, t, r) {
        r.d(t, {
            f: function() {
                return m
            }
        });
        var n = r(98601)
          , a = r(52088)
          , i = r(92379)
          , s = r(15478)
          , l = r(651);
        let o = ["icon", "children"];
        function c(e, t) {
            var r = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var n = Object.getOwnPropertySymbols(e);
                t && (n = n.filter(function(t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                })),
                r.push.apply(r, n)
            }
            return r
        }
        function d(e) {
            for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? c(Object(r), !0).forEach(function(t) {
                    (0,
                    n.Z)(e, t, r[t])
                }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : c(Object(r)).forEach(function(t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                })
            }
            return e
        }
        let u = s.Z.button`flex h-10 w-full items-center gap-2.5 rounded-lg px-2 text-token-text-primary hover:bg-token-sidebar-surface-secondary`
          , m = (0,
        i.forwardRef)(function(e, t) {
            let {icon: r, children: n} = e
              , i = (0,
            a.Z)(e, o);
            return (0,
            l.jsxs)(u, d(d({
                ref: t
            }, i), {}, {
                children: [(0,
                l.jsx)("div", {
                    className: "flex h-6 w-6 items-center justify-center text-token-text-secondary",
                    children: (0,
                    l.jsx)(r, {
                        className: "icon-md"
                    })
                }), (0,
                l.jsx)("span", {
                    className: "text-sm",
                    children: n
                })]
            }))
        })
    },
    22591: function(e, t, r) {
        r.d(t, {
            j: function() {
                return s
            }
        });
        var n = r(88667)
          , a = r(92379)
          , i = r(24241);
        function s() {
            let {conversations: e} = (0,
            i.MO)()
              , t = (0,
            a.useMemo)( () => !(e.length <= 5) && n.m9.checkGate("4277113861"), [e]);
            return {
                canUseHistoryIsCollapsible: t,
                isCollapsible: t && e.length > 5,
                recentConversationLimit: 5
            }
        }
    },
    60464: function(e, t, r) {
        r.d(t, {
            F: function() {
                return n
            }
        });
        let n = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
    }
}]);
//# sourceMappingURL=3127-9c874d12f71f51da.js.map
