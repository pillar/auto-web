/**
 * 小云雀 (Xiao Yun Que) Driver Logic
 * URL: https://xyq.jianying.com
 */
window.autoWeb_xyq = {
    sendPrompt: async (text) => {
        // Find input (usually a textarea or a rich text editor)
        const input = document.querySelector("textarea[placeholder*='描述']") || 
                      document.querySelector("div[contenteditable='true']") ||
                      document.querySelector(".lv-input-textarea");
        
        // The "Generate" button often shares the "Start Creating" text or a specific class
        const sendBtn = document.querySelector(".createButton-z2MuSL") || 
                        document.querySelector(".generate-btn") ||
                        document.querySelector("button:has-text('开始创作')");
        
        if (!input) throw new Error("XYQ input area not found");
        
        input.focus();
        // Clear existing if needed and insert
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, text);
        
        // Wait for state to sync
        await new Promise(r => setTimeout(r, 1000));
        
        if (sendBtn) {
            sendBtn.click();
            return { status: "sent", button_text: sendBtn.innerText };
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
