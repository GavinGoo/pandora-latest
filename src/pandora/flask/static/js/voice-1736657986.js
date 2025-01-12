!function () {
    async function go_voice() {
        const url = new URL(window.location.href);
        const model = url.searchParams.get('model') || '';
        console.log('Chat Model:', model);

        const response = await fetch('/api/voice/get_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({model})
        });

        const responseData = await response.json();
        if (responseData.url) {
            window.location.href = responseData.url;
        } else {
            throw new Error(responseData.detail || 'No URL provided by server');
        }
    }

    
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Voice Script Loaded');
        (async () => {
            const get_status = await fetch('/api/voice/get_status', {
                method: 'GET'
            });

            const get_status_data = await get_status.json();
            const voice_switch = get_status_data.status;

            if (voice_switch === true || voice_switch === 'true') {
                const logoId = 'closeai_voice_logo';
                let isVoiceActive = false;

                const style = document.createElement('style');
                style.textContent = `
                    @keyframes breathing {
                        0% { box-shadow: 0 0 5px 2px rgba(0, 123, 255, 0.4); }
                        50% { box-shadow: 0 0 15px 5px rgba(0, 123, 255, 0.6); }
                        100% { box-shadow: 0 0 5px 2px rgba(0, 123, 255, 0.4); }
                    }
                    .breathing-effect {
                        animation: breathing 5s ease-in-out infinite;
                        border-radius: 50%;
                    }
                `;
                document.head.appendChild(style);

                setInterval(() => {
                    if (document.getElementById(logoId)) {
                        return;
                    }

                    const textElements = document.querySelectorAll('div.flex.h-full > svg[role="img"].h-12.h-12 > text');
                    textElements.forEach(textElement => {
                        let x = parseFloat(textElement.getAttribute('x'));
                        let y = parseFloat(textElement.getAttribute('y'));

                        if (textElement.textContent.trim() === 'ChatGPT' && x < 0 && y < 0) {
                            console.log(textElement);
                            let svgElement = textElement.closest('svg');
                            if (svgElement && svgElement.id !== logoId) {
                                svgElement.id = logoId;
                                svgElement.style.cursor = 'pointer';
                                svgElement.classList.add('breathing-effect');
                                const handleVoiceClick = () => {
                                    if (isVoiceActive) {
                                        console.log('Voice is already active');
                                        return;
                                    }

                                    isVoiceActive = true;
                                    go_voice().catch(error => {
                                        alert('Failed to get voice link: ' + error.message);
                                        isVoiceActive = false;
                                    });
                                };

                                svgElement.addEventListener('click', handleVoiceClick);
                                svgElement.addEventListener('touchstart', handleVoiceClick);
                            }
                        }
                    });
                }, 1000);
            }
        })();
    });
}();
