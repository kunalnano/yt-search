#!/usr/bin/env python3
"""
Main entry point for yt-search terminal application
"""

import sys
import argparse
from .search import YouTubeSearcher
from .display import Display
from .utils import Colors as C

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='YT-Search: Algorithm-free YouTube terminal browser',
        epilog='No algorithms. No tracking. Just pure search.'
    )
    parser.add_argument('query', nargs='*', help='Search query (optional, enters interactive mode if omitted)')
    parser.add_argument('-n', '--max-results', type=int, default=20, help='Maximum results (default: 20)')
    parser.add_argument('-s', '--sort', choices=['views', 'date', 'relevance'], default='views', 
                       help='Sort order (default: views)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Force interactive mode')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # Join query parts
    query = ' '.join(args.query) if args.query else None
    
    if query and not args.interactive:
        # Direct search mode
        searcher = YouTubeSearcher()
        display = Display()
        
        print(f"\n{C.C}[SEARCHING]{C.X} {query}")
        results = searcher.search(query, max_results=args.max_results)
        display.show_results(results)
    else:
        # Interactive mode
        interactive_mode()

def interactive_mode():
    """Run interactive search mode"""
    searcher = YouTubeSearcher()
    display = Display()
    
    # Print banner
    display.show_banner()
    
    print(f"\n{C.G}Commands:{C.X}")
    print(f"  {C.C}search <query>{C.X} - Search YouTube (auto-sorted by views)")
    print(f"  {C.C}open <number>{C.X} - Open video in browser")
    print(f"  {C.C}url <number>{C.X} - Copy video URL")
    print(f"  {C.C}info <number>{C.X} - Show video details")
    print(f"  {C.C}quit{C.X} - Exit\n")
    
    current_results = []
    
    while True:
        try:
            prompt = f"{C.M}[YT-SEARCH]{C.X} > "
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command in ['quit', 'exit', 'q']:
                print(f"{C.G}[GOODBYE]{C.X}")
                break
            
            elif command in ['search', 's'] and len(parts) > 1:
                query = parts[1]
                current_results = searcher.search(query)
                display.show_results(current_results)
            
            elif command in ['open', 'o'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        display.open_video(current_results[index])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command in ['url', 'u'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        display.copy_url(current_results[index])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command in ['info', 'i'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        display.show_info(current_results[index])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command == 'help':
                display.show_help()
            
            else:
                # Treat as search query
                if command and not command.startswith('#'):
                    current_results = searcher.search(user_input)
                    display.show_results(current_results)
        
        except KeyboardInterrupt:
            print(f"\n{C.Y}[INTERRUPTED]{C.X}")
            continue
        except EOFError:
            print(f"\n{C.G}[GOODBYE]{C.X}")
            break

if __name__ == "__main__":
    main()
