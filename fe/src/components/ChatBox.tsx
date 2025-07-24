import { Box, Skeleton, Stack, TextField, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { useState, useEffect } from "react";

interface ChatHistory {
  role: 'user'|'assistant' | 'system';
  content: string
}

const ChatBox = () => {
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatHistory[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [streamingContent, setStreamingContent] = useState("");
  const theme = useTheme();

  useEffect(() => {
    console.log('Streaming content changed:', streamingContent);
  }, [streamingContent]);

  const handleKeyDown = async(e: React.KeyboardEvent<HTMLInputElement>) => {
    if(e.key === 'Enter' && chatInput.trim()) {
      const userMessage: ChatHistory = {role: 'user', content: chatInput};
      setChatHistory(prev => [...prev, userMessage]);
      setChatInput('');
      setLoading(true);
      setStreamingContent(""); // 重置流式内容
      
      try {
        const response = await fetch('http://localhost:8000/api/v1/qa', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream',
          },
          body: JSON.stringify({
            history: chatHistory,
            message: chatInput,
          })
        });

        if (!response.body) {
          throw new Error('No response body');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let accumulatedContent = ''; 
        
        if (reader) {
          while(true){
            const { done, value } = await reader.read();
            if(done) break;
            const chunk = decoder.decode(value, { stream: true });
            accumulatedContent += chunk; 
            setStreamingContent(accumulatedContent); 
          }
        }
        
        setChatHistory(prev => [...prev, {role: 'assistant', content: accumulatedContent}]);
        setStreamingContent(""); 
        setLoading(false);
        
      } catch (error) {
        console.error('Error sending message:', error);
        setLoading(false);
        setStreamingContent("");
      }
    }
  }

  return (
    <Box
      sx={{
        height: "100vh",
        width: "100vw",
        backgroundColor: theme.palette.background.default,
        color: theme.palette.text.primary,
        p: 2,
      }}
    >
      <Stack
        direction="column"
        spacing={2}
        sx={{ height: "calc(100vh - 100px)" }}
      >
        <Box
          sx={{
            flex: 1,
            border: `2px solid ${theme.palette.primary.main}`,
            borderRadius: 1,
            p: 2,
            backgroundColor: theme.palette.background.paper,
            overflow: 'auto'
          }}
        >
          <Typography sx={{ fontSize: "1.5rem", mb: 2 }}>
            Chat Messages Area
          </Typography>
          
          {chatHistory.map((chat, index) => (
            <Box 
              key={index} 
              sx={{
                mb: 2,
                p: 2,
                borderRadius: 1,
                backgroundColor: chat.role === 'user' 
                  ? theme.palette.primary.main 
                  : theme.palette.background.default,
                color: chat.role === 'user' 
                  ? theme.palette.primary.contrastText 
                  : theme.palette.text.primary,
                border: `1px solid ${theme.palette.primary.main}`,
              }}
            >
              <Typography variant="body1">
                <strong>{chat.role}:</strong> {chat.content}
              </Typography>
            </Box>
          ))}
          
          {streamingContent && (
            <Box 
              sx={{
                mb: 2,
                p: 2,
                borderRadius: 1,
                backgroundColor: theme.palette.background.default,
                color: theme.palette.text.primary,
                border: `1px solid ${theme.palette.primary.main}`,
              }}
            >
              <Typography variant="body1">
                <strong>assistant:</strong> {streamingContent}
              </Typography>
            </Box>
          )}
          
          {loading && !streamingContent && (
            <Box sx={{
              p: 2,
              borderRadius: 1,
              backgroundColor: theme.palette.background.default,
              border: `1px solid ${theme.palette.primary.main}`,
            }}>
              <Skeleton variant="text" width="100%" height={20} />
              <Skeleton variant="text" width="80%" height={20} />
              <Skeleton variant="text" width="60%" height={20} />
            </Box>
          )}
        </Box>

        <TextField
          id='chat-input'
          placeholder='Type your message and press Enter...'
          multiline
          maxRows={3}
          disabled={loading}
          sx={{
            '& .MuiOutlinedInput-root': {
              backgroundColor: theme.palette.background.paper,
              border: `2px solid ${theme.palette.primary.main}`,
              borderRadius: 1,
              '& fieldset': {
                border: 'none',
              },
              '&:hover fieldset': {
                border: 'none',
              },
              '&.Mui-focused fieldset': {
                border: 'none',
              },
            },
            '& .MuiInputBase-input': {
              color: theme.palette.text.primary,
              fontSize: "1rem",
            },
            '& .MuiInputBase-input::placeholder': {
              color: theme.palette.text.secondary,
            },
          }}
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </Stack>
    </Box>
  );
};

export default ChatBox;
