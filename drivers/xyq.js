/**
 * 小云雀 (Xiao Yun Que) Driver Logic
 * URL: https://xyq.jianying.com
 */
window.autoWeb_xyq = {
    sendPrompt: async (text) => {
        // Find input (usually a textarea or a rich text editor)
        const input = document.querySelector("textarea[placeholder*='描述']") || 
                      document.querySelector("div[contenteditable='true']");
        const sendBtn = document.querySelector("button[class*='send']") || 
                        document.querySelector(".generate-btn");
        
        if (!input) throw new Error("XYQ input area not found");
        
        input.focus();
        document.execCommand('insertText', false, text);
        
        // Jianying tools often need a small delay for state update
        await new Promise(r => setTimeout(r, 800));
        
        if (sendBtn) {
            sendBtn.click();
            return { status: "sent" };
        }
        return { status: "button_not_found" };
    },
    
    // Example: Automate Login (requires phone input from user)
    fillLogin: (phone) => {
        const phoneInput = document.querySelector("input[placeholder*='手机号']");
        if (phoneInput) {
            phoneInput.value = phone;
            phoneInput.dispatchEvent(new Event('input', { bubbles: true }));
            return { status: "phone_filled" };
        }
        return { status: "login_field_not_found" };
    }
};
