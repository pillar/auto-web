/**
 * Doubao Driver Logic
 * Injected via CDP/Playwright
 */
window.autoWeb_doubao = {
    sendPrompt: async (text) => {
        // Try multiple selector patterns for Doubao input
        const input = document.querySelector("div[contenteditable='true']") || 
                      document.querySelector("textarea[placeholder*='发消息']") ||
                      document.querySelector(".semi-input-textarea") ||
                      document.querySelector("textarea");
        
        // Find send button
        const sendBtn = document.querySelector("button[data-testid='chat_send_button']") ||
                        document.querySelector("button[class*='send']");
        
        if (!input) throw new Error("Doubao input area not found");
        
        input.focus();
        // Clear and Insert
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, text);
        
        // Wait for potential UI state change
        await new Promise(r => setTimeout(r, 1000));
        
        if (sendBtn) {
            sendBtn.click();
            return { status: "sent" };
        } else {
            // Fallback: Press Enter
            const enterEvent = new KeyboardEvent('keydown', {
                key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
            });
            input.dispatchEvent(enterEvent);
            return { status: "sent_via_enter" };
        }
    }
};
