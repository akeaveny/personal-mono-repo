# Start a new session named "claude"                    
tmux new -s claude                             

# Inside tmux, start claude as normal                   
claude --dangerously-skip-permissions                   
# then type /remote-control                             

# Detach (session keeps running in background): Ctrl+B, 
then D                                                  

# Reattach later                                        
tmux attach -t claude  