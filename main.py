import discord
import os
from discord import app_commands
from discord import message
from discord.ext import commands
import random
from discord.ext.commands.hybrid import U
import requests
import time
from discord.ui import Button, View
import chess
import chess.svg
import sys
from stockfish import Stockfish
import chess.engine
import time
import cairosvg

engine = chess.engine.SimpleEngine.popen_uci(r"/opt/homebrew/Cellar/stockfish/16/bin/stockfish")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!Meher', intents=intents)

@bot.event
async def on_connect():
  print("Your bot is online")
  try:
    synced=await bot.tree.sync()
    print("synced " + str(len(synced)) + " command(s)")
  except Exception as e:
    print(e)


def save_chessboard_as_png(board, filename):
    # Generate SVG representation of the board
    svg_content = chess.svg.board(board=board)
  
    # Save the SVG content to a file
    with open('chess_board.svg', 'w') as svg_file:
        svg_file.write(svg_content)
  
    # Convert the SVG file to PNG using CairoSVG
    cairosvg.svg2png(url='chess_board.svg', write_to='chessboard.png')




@bot.tree.command(name='cc')
async def cc(interaction):
    button1 = Button(label="Play Human", style=discord.ButtonStyle.green)
    button2 = Button(label="Play Stockfish", style=discord.ButtonStyle.green)
    button3 = Button(label="Watch Computer VS Computer", style=discord.ButtonStyle.green)


    button1.callback = chessGameRun
    button2.callback = stockfishGameRun
    button3.callback = CvsC
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await interaction.response.send_message("Press button to play chess game:", view=view)

async def CvsC(interaction):
    board = chess.Board()
    await interaction.response.send_message("Starting AI VS AI")
    count = 0
    num1 = 0

    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        time.sleep(0.2)

        # Save and send the updated chessboard image
        save_chessboard_as_png(board, "chessboard.png")
        with open('chessboard.png', 'rb') as f:
            picture = discord.File(f)
            await interaction.followup.send(file=picture)
        count += 1 
		
    await interaction.followup.send("There were " + str(count) + " moves.")

@bot.tree.command(name = "mehersocialmediaeffects")
async def mehersocialmediaeffects(interaction):
    social_media_effects = ['Social media intentionally increases your dopamine levels to keep you interacting with the app', 
    'Social media promotes unrealistic body shape goals and can damage mental health', 
    'Sites like Facebook and Instagram can exacerbate feelings of inadequacy and comparison']

    await interaction.response.send_message("Social Media Affects")
    await interaction.followup.send("1.) " + social_media_effects[0])
    await interaction.followup.send("2.) " + social_media_effects[1])
    await interaction.followup.send("3.) " + social_media_effects[2])


@bot.tree.command(name = "mehersocailmediafacts")
async def mehersocailmediafacts(interaction):
  responses = ['Social media intentionally increases your dopamine levels periodically to keep you interacting with the app', 'Social media has unrealistic body shape goals and it damages your mental health', "The Silicon Valley is a place where people are more likely to be successful than the rest of the world", "Computer Science jobs are in high demand", "The average software engineer in Silicon Valley earns about $165,000 a year", "Computer science is the study of computers and computational systems, including their design, development, and application", "The average software engineer in Silicon Valley earns about $165,000", "The best universities for computer science are: Stanford University, University of California, Berkeley, Carnegie Mellon", "Multiple studies have found a strong link between heavy social media and an increased risk for depression, anxiety, loneliness, self-harm, and even suicidal thoughts.", "If you’re spending an excessive amount of time on social media and feelings of sadness, dissatisfaction, frustration, or loneliness are impacting your life, it may be time to re-examine your online habits and find a healthier balance.", "Tech jobs aren’t simply growing—they’re skyrocketing. This cluster of careers is projected to grow by 13 percent between 2016 and 2026, according to the Bureau of Labor Statistics (BLS).2 That’s much faster than the average rate of growth for all occupations, which is seven percent.", "Our analysis of software development and computer programming job postings show that just over 88 percent of employers are seeking candidates with a Bachelor’s degree", "Going into a technology career doesn’t mean you have to work within the technology industry. Computer science jobs abound in all kinds of industries. Software is a tool that can be useful in nearly any field.", "If there’s one thing the last 20 years have shown us, it’s that technology’s always evolving. As a professional in the space, you’ll keep a pulse on the latest advancements. And, who knows? You might just end up on the next team to develop life-changing tech. The possibilities are truly endless!", "Sites such as Facebook and Instagram seem to exacerbate feelings that others are having more fun or living better lives than you are.", "About 10 percent of teens report being bullied on social media and many other users are subjected to offensive comments. Social media platforms such as Twitter can be hotspots for spreading hurtful rumors, lies, and abuse that can leave lasting emotional scars.", "Sharing endless selfies and all your innermost thoughts on social media can create an unhealthy self-centeredness and distance you from real-life connections."]
  print(len(responses))
  choosefact = random.randint(0,16)
  await interaction.response.send_message(responses[choosefact])


async def stockfishGameRun(interaction):
  await interaction.response.send_message("Chess Game Starts You Verus Stockfish")
  board = chess.Board()
  num = 0 
  save_chessboard_as_png(board, "chessboard.png")
  with open('chessboard.png', 'rb') as f:
    picture = discord.File(f)
    await interaction.followup.send(file=picture)
  while not board.is_game_over():
    if num == 1:
      print(chess.svg.board(board=board))
      move_input = ""
      await interaction.followup.send("Enter your move:")
      not_done = True
      while not_done:
          msg = await bot.wait_for("message")
          if msg.content.startswith("-cb "):
              move_input = msg.content[4:]
              not_done = False
          elif msg.content.startswith("draw"):
            await interaction.followup.send("draw???")
            save_chessboard_as_png(board, "chessboard.png")
            with open('chessboard.png', 'rb') as f:
              picture = discord.File(f)
              await interaction.followup.send(file=picture)
            sys.exit(0)
  
          elif msg.content.startswith("resign"):
            await interaction.followup.send("You lose")
            save_chessboard_as_png(board, "chessboard.png")
            with open('chessboard.png', 'rb') as f:
              picture = discord.File(f)
              await interaction.followup.send(file=picture)
            sys.exit(0)
      try:
        move = chess.Move.from_uci(move_input)
        if move in board.legal_moves:
            board.push(move)
            num = 0 
            save_chessboard_as_png(board, "chessboard.png")
            with open('chessboard.png', 'rb') as f:
              picture = discord.File(f)
              await interaction.followup.send(file=picture)
        elif num == 0:
            await interaction.followup.send("Invalid move! Try again.")
            if board.is_check() and not board.is_checkmate():
              await interaction.followup.send("You are in check! Keep that in mind.")
              save_chessboard_as_png(board, "chessboard.png")
              with open('chessboard.png', 'rb') as f:
                picture = discord.File(f)
                await interaction.followup.send(file=picture)
      except ValueError:
        print("Invalid input format! Please provide a move in algebraic notation (e.g., 'e2e4').")
    else:
      result = engine.play(board, chess.engine.Limit(time=0.1))
      board.push(result.move)
      num = 1
      time.sleep(0.1)
      save_chessboard_as_png(board, "chessboard.png")
      with open('chessboard.png', 'rb') as f:
        picture = discord.File(f)
        await interaction.followup.send(file=picture)
    

  await interaction.followup.send("Game over!")
  if board.is_checkmate and board.turn == "WHITE":
    await interaction.followup.send("Checkmate! You win!")

    save_chessboard_as_png(board, "chessboard.png")
    with open('chessboard.png', 'rb') as f:
      picture = discord.File(f)
      await interaction.followup.send(file=picture)
  elif not board.is_checkmate:
    await interaction.followup.send("Stalemate! It's a draw!")

    save_chessboard_as_png(board, "chessboard.png")
    with open('chessboard.png', 'rb') as f:
      picture = discord.File(f)
      await interaction.followup.send(file=picture)
  else:
    await interaction.followup.send("Checkmate! You lose!")

  save_chessboard_as_png(board, "chessboard.png")
  with open('chessboard.png', 'rb') as f:
    picture = discord.File(f)
    await interaction.followup.send(file=picture)

    

  await interaction.followup.send("Game over!")
  if board.is_checkmate and board.turn == "WHITE":
    await interaction.followup.send("Checkmate! You win!")

    save_chessboard_as_png(board, "chessboard.png")
    with open('chessboard.png', 'rb') as f:
      picture = discord.File(f)
      await interaction.followup.send(file=picture)
  elif not board.is_checkmate:
    await interaction.followup.send("Stalemate! It's a draw!")

    save_chessboard_as_png(board, "chessboard.png")
    with open('chessboard.png', 'rb') as f:
      picture = discord.File(f)
      await interaction.followup.send(file=picture)
  else:
    await interaction.followup.send("Checkmate! You lose!")

  save_chessboard_as_png(board, "chessboard.png")
  with open('chessboard.png', 'rb') as f:
    picture = discord.File(f)
    await interaction.followup.send(file=picture)


async def chessGameRun(interaction):
  await interaction.response.send_message("Chess Game Starts")
  board = chess.Board()
  save_chessboard_as_png(board, "chessboard.png")
  with open('chessboard.png', 'rb') as f:
    picture = discord.File(f)
    await interaction.followup.send(file=picture)
  while not board.is_game_over():
    print(chess.svg.board(board=board))
    move_input = ""
    await interaction.followup.send("Enter your move:")
    not_done = True
    while not_done:
        msg = await bot.wait_for("message")
        if msg.content.startswith("-cb "):
            move_input = msg.content[4:]
            not_done = False
        elif msg.content.startswith("draw"):
          await interaction.followup.send("draw???")
          save_chessboard_as_png(board, "chessboard.png")
          with open('chessboard.png', 'rb') as f:
            picture = discord.File(f)
            await interaction.followup.send(file=picture)
          sys.exit(0)

        elif msg.content.startswith("resign"):
          await interaction.followup.send("You lose")
          save_chessboard_as_png(board, "chessboard.png")
          with open('chessboard.png', 'rb') as f:
            picture = discord.File(f)
            await interaction.followup.send(file=picture)
          sys.exit(0)


    try:
        move = chess.Move.from_uci(move_input)
        if move in board.legal_moves:
            board.push(move)
            save_chessboard_as_png(board, "chessboard.png")
            with open('chessboard.png', 'rb') as f:
              picture = discord.File(f)
              await interaction.followup.send(file=picture)
        else:
            await interaction.followup.send("Invalid move! Try again.")
            if board.is_check() and not board.is_checkmate():
              await interaction.followup.send("You are in check! Keep that in mind.")
              save_chessboard_as_png(board, "chessboard.png")
              with open('chessboard.png', 'rb') as f:
                picture = discord.File(f)
                await interaction.followup.send(file=picture)
    except ValueError:
        print("Invalid input format! Please provide a move in algebraic notation (e.g., 'e2e4').")
  await interaction.followup.send("Game over!")
  if board.is_checkmate and board.turn == "WHITE":
    await interaction.followup.send("Checkmate! You win!")

    save_chessboard_as_png(board, "chessboard.png")
    with open('chessboard.png', 'rb') as f:
      picture = discord.File(f)
      await interaction.followup.send(file=picture)
  elif not board.is_checkmate:
    await interaction.followup.send("Stalemate! It's a draw!")

    save_chessboard_as_png(board, "chessboard.png")
    with open('chessboard.png', 'rb') as f:
      picture = discord.File(f)
      await interaction.followup.send(file=picture)
  else:
    await interaction.followup.send("Checkmate! You lose!")

  save_chessboard_as_png(board, "chessboard.png")
  with open('chessboard.png', 'rb') as f:
    picture = discord.File(f)
    await interaction.followup.send(file=picture)


bot_token = os.environ.get('DISCORD_BOT_TOKEN')

if bot_token is None:
    print("Please set the DISCORD_BOT_TOKEN environment variable.")
else:
    bot.run(bot_token)



