/**
 * Gemini Driver Logic
 */
window.autoWeb_gemini = {
    sendPrompt: async (text) => {
        const input = document.querySelector("div[contenteditable='true'][role='textbox']");
        const sendBtn = document.querySelector("button[aria-label*='Send']");
        
        if (!input) throw new Error("Gemini input field not found");
        
        input.focus();
        document.execCommand('insertText', false, text);
        
        // Wait a bit for the send button to become active
        await new Promise(r => setTimeout(r, 500));
        
        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
            return { status: "sent" };
        }
        return { status: "failed_to_click_button" };
    }
};
