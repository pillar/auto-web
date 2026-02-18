/**
 * Doubao Driver Logic
 * Injected via CDP/Playwright
 */
window.autoWeb_doubao = {
    sendPrompt: async (text) => {
        const input = document.querySelector("div[contenteditable='true']");
        const sendBtn = document.querySelector("button[data-testid='chat_send_button']");
        
        if (!input) throw new Error("Input not found");
        
        // Use native events for safety
        input.focus();
        document.execCommand('insertText', false, text);
        
        if (sendBtn) {
            sendBtn.click();
            return { status: "sent" };
        } else {
            // Fallback to Enter key
            const event = new KeyboardEvent('keydown', {
                key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: True
            });
            input.dispatchEvent(event);
            return { status: "sent_via_enter" };
        }
    }
};
