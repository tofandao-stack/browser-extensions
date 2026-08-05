const HOST_NAME = "com.costel.youtube_mp3";

chrome.action.onClicked.addListener(async (tab) => {
  try {
    const url = tab?.url || "";

    if (!url) {
      console.error("Nu am găsit URL-ul tabului curent.");
      return;
    }

    const allowed =
      url.startsWith("https://www.youtube.com/") ||
      url.startsWith("https://youtu.be/") ||
      url.startsWith("https://music.youtube.com/");

    if (!allowed) {
      console.error("Tabul curent nu este YouTube.");
      return;
    }

    const response = await chrome.runtime.sendNativeMessage(HOST_NAME, {
      action: "download",
      url: url
    });

    console.log("Răspuns host:", response);
  } catch (err) {
    console.error("Eroare la trimiterea către host:", err);
  }
});
