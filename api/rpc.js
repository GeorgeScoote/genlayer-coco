// =================================================================
// 文件: rpc.js (最终版)
// =================================================================

const CONTRACT_ID = "0xF7201Bb19FE8203767fa5F02c37EA8a0C84AcaBa"; // ！！！请务必替换成您自己的合约ID ！！！

async function getGameStatus() {
    if (!window.genLayer) { console.error("Genlayer钱包未连接。"); alert("Genlayer钱包未连接，请先连接钱包！"); return null; }
    try {
        const response = await window.genLayer.public.view({ contract: CONTRACT_ID, method: "get_game_status", args: [] });
        if (response && response.result) { const gameStatus = JSON.parse(response.result); return gameStatus; } 
        else { console.error("获取游戏状态失败:", response); return null; }
    } catch (error) { console.error("调用 get_game_status 时发生错误:", error); return null; }
}

async function submitWord(word) {
    if (!window.genLayer) { console.error("Genlayer钱包未连接。"); alert("Genlayer钱包未连接，请先连接钱包！"); return null; }
    if (!word || typeof word !== 'string' || word.trim() === '') { alert("请输入一个有效的单词！"); return null; }
    try {
        const response = await window.genLayer.public.write({ contract: CONTRACT_ID, method: "submit_word", args: [word.trim()] });
        alert("单词提交成功！请等待几秒钟让区块链确认。");
        return response;
    } catch (error) {
        console.error("调用 submit_word 时发生错误:", error);
        if (error.message && error.message.includes("Already submitted")) { alert("提交失败：您已经在此轮游戏中提交过单词了。"); } 
        else { alert("提交单词失败，请检查浏览器控制台获取更多信息。"); }
        return null;
    }
}

async function getLeaderboard() {
    if (!window.genLayer) { console.error("Genlayer钱包未连接。"); return null; }
    try {
        const response = await window.genLayer.public.view({ contract: CONTRACT_ID, method: "get_leaderboard", args: [] });
        if (response && response.result) { const leaderboard = JSON.parse(response.result); return leaderboard; } 
        else { console.error("获取排行榜失败:", response); return null; }
    } catch (error) { console.error("调用 get_leaderboard 时发生错误:", error); return null; }
}
