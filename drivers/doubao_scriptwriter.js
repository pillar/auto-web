/**
 * Doubao Scriptwriting Driver
 * Automated short drama script generation
 */
window.autoWeb_doubao_scriptwriter = {
    // Main entry: write a short drama script
    writeScript: async (params) => {
        const { title, genre, scenes, characters, tone, length } = params;
        
        // Step 1: Click "帮我写作" (Help me write) skill
        const writingBtn = document.querySelector('button:has-text("帮我写作")') ||
                          document.querySelector('[class*="writing"]') ||
                          document.querySelector('button[class*="skill"]:has-text("写作")');
        
        if (writingBtn) {
            writingBtn.click();
            await new Promise(r => setTimeout(r, 2000));
        }
        
        // Step 2: Find input and construct script prompt
        const input = document.querySelector("div[contenteditable='true']") || 
                      document.querySelector("textarea[placeholder*='发消息']") ||
                      document.querySelector("textarea");
        
        if (!input) throw new Error("Scriptwriting input not found");
        
        // Construct professional script prompt
        const scriptPrompt = `请为我创作一部短剧剧本：
剧名：《${title || '未命名'}》
类型：${genre || '都市情感'}
场次：${scenes || '10'}场
主要角色：${characters || '2-3人'}
风格基调：${tone || '轻松幽默'}
篇幅：${length || '每集1-2分钟，共10集'}

要求：
1. 符合抖音/快手短剧爆款结构（黄金3秒开头+反转剧情+悬念结尾）
2. 每集都要有冲突点和情绪爆点
3. 台词要口语化、有网络感
4. 标注场景和人物动作

请直接输出完整剧本格式。`;
        
        // Step 3: Input the prompt
        input.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, scriptPrompt);
        
        await new Promise(r => setTimeout(r, 1000));
        
        // Step 4: Send
        const sendBtn = document.querySelector("button[data-testid='chat_send_button']") ||
                        document.querySelector("button[class*='send']");
        
        if (sendBtn) {
            sendBtn.click();
            return { status: "script_request_sent", mode: "writing" };
        } else {
            const enterEvent = new KeyboardEvent('keydown', {
                key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
            });
            input.dispatchEvent(enterEvent);
            return { status: "script_request_sent_via_enter", mode: "writing" };
        }
    },
    
    // Quick script with minimal params
    quickScript: async (idea) => {
        const input = document.querySelector("div[contenteditable='true']") || 
                      document.querySelector("textarea");
        
        if (!input) throw new Error("Input not found");
        
        const prompt = `请帮我写一个短剧剧本，核心创意是：${idea}
要求：有冲突、有反转、适合拍成1分钟短视频。直接输出剧本格式。`;
        
        input.focus();
        document.execCommand('insertText', false, prompt);
        
        await new Promise(r => setTimeout(r, 800));
        
        const enterEvent = new KeyboardEvent('keydown', {
            key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
        });
        input.dispatchEvent(enterEvent);
        
        return { status: "quick_script_sent", idea: idea };
    }
};
