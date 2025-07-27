import {
  Box,
  Skeleton,
  TextField,
  Typography,
  Avatar,
  IconButton,
  Paper,
} from "@mui/material";
import { useTheme, type Theme } from "@mui/material/styles";
import { useState, useEffect } from "react";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import RefreshIcon from "@mui/icons-material/Refresh";
import SendIcon from "@mui/icons-material/Send";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Chat message interface
interface ChatHistory {
  role: "user" | "assistant" | "system";
  content: string;
}

// Reusable markdown styles for consistent rendering
const getMarkdownStyles = (theme: Theme) => ({    
  lineHeight: 1.6,
  wordBreak: "break-word",
  "& h1, & h2, & h3, & h4, & h5, & h6": {
    color: theme.palette.text.primary,
    marginTop: 2,
    marginBottom: 1,
  },
  "& p": {
    marginBottom: 1,
  },
  "& code": {
    backgroundColor: theme.palette.action.hover,
    padding: "2px 4px",
    borderRadius: 1,
    fontSize: "0.875em",
  },
  "& pre": {
    backgroundColor: theme.palette.background.default,
    padding: 2,
    borderRadius: 1,
    overflow: "auto",
    marginBottom: 1,
  },
  "& pre code": {
    backgroundColor: "transparent",
    padding: 0,
  },
  "& blockquote": {
    borderLeft: `4px solid ${theme.palette.primary.main}`,
    paddingLeft: 2,
    marginLeft: 0,
    marginRight: 0,
    fontStyle: "italic",
    color: theme.palette.text.secondary,
  },
  "& ul, & ol": {
    paddingLeft: 3,
    marginBottom: 1,
  },
  "& li": {
    marginBottom: 0.5,
  },
  "& table": {
    borderCollapse: "collapse",
    width: "100%",
    marginBottom: 1,
  },
  "& th, & td": {
    border: `1px solid ${theme.palette.divider}`,
    padding: 1,
    textAlign: "left",
  },
  "& th": {
    backgroundColor: theme.palette.action.hover,
  },
  "& a": {
    color: theme.palette.secondary.main,
    textDecoration: "none",
    "&:hover": {
      textDecoration: "underline",
      color: theme.palette.secondary.light || theme.palette.secondary.main,
    },
    "&:visited": {
      color: theme.palette.secondary.main,
    },
  },
});

// Reusable avatar component
const ChatAvatar = ({ role, theme }: { role: string; theme: Theme }) => (
  <Avatar
    sx={{
      width: 32,
      height: 32,
      backgroundColor: role === "user" 
        ? theme.palette.primary.main 
        : theme.palette.secondary.main,
      color: theme.palette.primary.contrastText,
      fontSize: "14px",
      fontWeight: "bold",
    }}
  >
    {role === "user" ? "Q" : "A"}
  </Avatar>
);

// Reusable message content component with markdown support
const MessageContent = ({
  content,
  isAssistant,
  theme,
}: {
  content: string;
  isAssistant: boolean;
  theme: Theme;
}) => {
  if (isAssistant) {
    return (
      <Box sx={getMarkdownStyles(theme)}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </Box>
    );
  }

  return (
    <Typography
      variant="body1"
      sx={{
        lineHeight: 1.6,
        whiteSpace: "pre-wrap",
        wordBreak: "break-word",
      }}
    >
      {content}
    </Typography>
  );
};

// Reusable action buttons component
const ActionButtons = ({
  onCopy,
  onRegenerate,
  loading,
  theme,
}: {
  onCopy: () => void;
  onRegenerate: () => void;
  loading: boolean;
  theme: Theme;
}) => (
  <Box
    sx={{
      mt: 2,
      display: "flex",
      gap: 1,
      alignItems: "center",
    }}
  >
    <IconButton
      size="small"
      onClick={onCopy}
      sx={{ color: theme.palette.text.secondary }}
    >
      <ContentCopyIcon fontSize="small" />
    </IconButton>
    <IconButton
      size="small"
      onClick={onRegenerate}
      disabled={loading}
      sx={{ color: theme.palette.text.secondary }}
    >
      <RefreshIcon fontSize="small" />
    </IconButton>
  </Box>
);

// Reusable welcome message component
const WelcomeMessage = ({ theme }: { theme: Theme }) => (
  <Box
    sx={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      color: theme.palette.text.secondary,
    }}
  >
    <Typography variant="h4" sx={{ mb: 2, fontWeight: 600 }}>
      ACS Chat
    </Typography>
    <Box
      sx={{
        textAlign: "center",
        maxWidth: 500,
        margin: "0 auto",
        fontSize: "12px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        This assistant answers questions about the **ACS skills assessment for
        Australian skilled migration** only. Unrelated queries won't be
        processed.
      </ReactMarkdown>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        **Note:** Chat history clears on page refresh.
      </ReactMarkdown>
    </Box>
  </Box>
);

// Reusable input area component
const InputArea = ({
  chatInput,
  setChatInput,
  handleSendMessage,
  handleKeyDown,
  loading,
  theme,
}: {
  chatInput: string;
  setChatInput: (value: string) => void;
  handleSendMessage: () => void;
  handleKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  loading: boolean;
  theme: Theme;
}) => (
  <Box
    sx={{
      borderTop: `1px solid ${theme.palette.divider}`,
      backgroundColor: theme.palette.background.default,
      p: 2,
    }}
  >
    <Box
      sx={{
        maxWidth: "800px",
        margin: "0 auto",
        position: "relative",
      }}
    >
      <Paper
        elevation={0}
        sx={{
          border: `1px solid ${theme.palette.divider}`,
          borderRadius: 2,
          backgroundColor: theme.palette.background.paper,
          p: 1,
          display: "flex",
          alignItems: "center",
          gap: 1,
          flexDirection: "row",
          justifyContent: "center",
        }}
      >
        <TextField
          multiline
          maxRows={4}
          disabled={loading}
          placeholder="Message ACS Chat..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={handleKeyDown}
          sx={{
            flex: 1,
            "& .MuiOutlinedInput-root": {
              border: "none",
              "& fieldset": {
                border: "none",
              },
              "&:hover fieldset": {
                border: "none",
              },
              "&.Mui-focused fieldset": {
                border: "none",
              },
            },
            "& .MuiInputBase-input": {
              color: theme.palette.text.primary,
              fontSize: "1rem",
              lineHeight: 1.5,
              padding: "8px 0",
            },
            "& .MuiInputBase-input::placeholder": {
              color: theme.palette.text.secondary,
            },
          }}
        />
        <IconButton
          onClick={handleSendMessage}
          disabled={!chatInput.trim() || loading}
          sx={{
            color:
              chatInput.trim() && !loading
                ? theme.palette.primary.main
                : theme.palette.text.secondary,
          }}
        >
          <SendIcon />
        </IconButton>
      </Paper>
      <Typography
        variant="caption"
        sx={{
          mt: 1,
          color: theme.palette.text.secondary,
          textAlign: "center",
          display: "block",
        }}
      >
        ACS Chat can make mistakes. Consider checking important information.
      </Typography>
    </Box>
  </Box>
);

// Main chat component
const ChatBox = () => {
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatHistory[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [streamingContent, setStreamingContent] = useState("");
  const theme = useTheme();

  // Debug streaming content changes
  useEffect(() => {
    console.log("Streaming content changed:", streamingContent);
  }, [streamingContent]);

  // Shared API call logic for both send and regenerate
  const callQAAPI = async (history: ChatHistory[], message: string) => {
    setLoading(true);
    setStreamingContent("");

    try {
      // Use relative path for API, works for both dev and prod with proxy
      const response = await fetch('/api/v1/qa', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "text/event-stream",
        },
        body: JSON.stringify({
          history,
          message,
        }),
      });

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let accumulatedContent = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          accumulatedContent += chunk;
          setStreamingContent(accumulatedContent);
        }
      }

      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: accumulatedContent },
      ]);
      setStreamingContent("");
      setLoading(false);
    } catch (error) {
      console.error("Error calling QA API:", error);
      setLoading(false);
      setStreamingContent("");
    }
  };

  // Handle sending new message
  const handleSendMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage: ChatHistory = { role: "user", content: chatInput };
    setChatHistory((prev) => [...prev, userMessage]);
    setChatInput("");

    await callQAAPI(chatHistory, chatInput);
  };

  // Handle keyboard events
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Copy message content to clipboard
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  // Regenerate the last AI response
  const regenerateResponse = async () => {
    // Remove the last AI response
    const newHistory = chatHistory.slice(0, -1);
    setChatHistory(newHistory);

    // Get the last user message
    const lastUserMessage = newHistory[newHistory.length - 1];
    if (lastUserMessage && lastUserMessage.role === "user") {
      // Use shared API call logic
      await callQAAPI(newHistory.slice(0, -1), lastUserMessage.content);
    }
  };

  return (
    <Box
      sx={{
        height: "100vh",
        width: "100vw",
        backgroundColor: theme.palette.background.default,
        color: theme.palette.text.primary,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Chat messages area */}
      <Box
        sx={{
          flex: 1,
          overflow: "auto",
          p: 0,
          backgroundColor: theme.palette.background.default,
        }}
      >
        {/* Show welcome message when no chat history */}
        {chatHistory.length === 0 && <WelcomeMessage theme={theme} />}

        {/* Render chat history */}
        {chatHistory.map((chat, index) => (
          <Box
            key={index}
            sx={{
              borderBottom: `1px solid ${theme.palette.divider}`,
              backgroundColor:
                chat.role === "user"
                  ? theme.palette.background.default
                  : theme.palette.background.paper,
            }}
          >
            <Box
              sx={{
                maxWidth: "800px",
                margin: "0 auto",
                p: 3,
                display: "flex",
                gap: 2,
              }}
            >
              <ChatAvatar role={chat.role} theme={theme} />
              <Box sx={{ flex: 1 }}>
                <MessageContent
                  content={chat.content}
                  isAssistant={chat.role === "assistant"}
                  theme={theme}
                />

                {/* Action buttons for AI responses */}
                {chat.role === "assistant" && (
                  <ActionButtons
                    onCopy={() => copyToClipboard(chat.content)}
                    onRegenerate={() => regenerateResponse()}
                    loading={loading}
                    theme={theme}
                  />
                )}
              </Box>
            </Box>
          </Box>
        ))}

        {/* Streaming content display */}
        {streamingContent && (
          <Box
            sx={{
              borderBottom: `1px solid ${theme.palette.divider}`,
              backgroundColor: theme.palette.background.paper,
            }}
          >
            <Box
              sx={{
                maxWidth: "800px",
                margin: "0 auto",
                p: 3,
                display: "flex",
                gap: 2,
              }}
            >
              <ChatAvatar role="assistant" theme={theme} />
              <Box sx={{ flex: 1 }}>
                <MessageContent
                  content={streamingContent}
                  isAssistant={true}
                  theme={theme}
                />
              </Box>
            </Box>
          </Box>
        )}

        {/* Loading state */}
        {loading && !streamingContent && (
          <Box
            sx={{
              borderBottom: `1px solid ${theme.palette.divider}`,
              backgroundColor: theme.palette.background.paper,
            }}
          >
            <Box
              sx={{
                maxWidth: "800px",
                margin: "0 auto",
                p: 3,
                display: "flex",
                gap: 2,
              }}
            >
              <ChatAvatar role="assistant" theme={theme} />
              <Box sx={{ flex: 1 }}>
                <Skeleton variant="text" width="100%" height={20} />
                <Skeleton variant="text" width="80%" height={20} />
                <Skeleton variant="text" width="60%" height={20} />
              </Box>
            </Box>
          </Box>
        )}
      </Box>

      {/* Input area */}
      <InputArea
        chatInput={chatInput}
        setChatInput={setChatInput}
        handleSendMessage={handleSendMessage}
        handleKeyDown={handleKeyDown}
        loading={loading}
        theme={theme}
      />
    </Box>
  );
};

export default ChatBox;
