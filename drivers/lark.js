/**
 * Lark (Feishu) Driver Logic
 */
window.autoWeb_lark = {
    sendPrompt: async (text) => {
        const input = document.querySelector(".rich_text_editor");
        const sendBtn = document.querySelector("button[data-testid='chat-send-button']");
        
        if (!input) throw new Error("Lark editor not found");
        
        input.focus();
        document.execCommand('insertText', false, text);
        
        if (sendBtn) {
            sendBtn.click();
            return { status: "sent" };
        }
        return { status: "button_not_found" };
    }
};
