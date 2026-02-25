// generate_dalle_images.js
// Usage:
//   export OPENAI_API_KEY="sk-..."
//   node script/generate_dalle_images.js
// This script calls the OpenAI Image Generation endpoint (DALL·E-like) to create PNG images
// and saves them to assets/images/*.png

import fs from 'fs';
import path from 'path';

const API_KEY = process.env.OPENAI_API_KEY;
if(!API_KEY){
  console.error('Missing OPENAI_API_KEY environment variable.');
  process.exit(1);
}

const outDir = path.resolve('assets/images');
if(!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const prompts = [
  {
    file: 'stress.png',
    prompt: 'Photorealistic scene of workplace stress: an adult in a call center desk shouting into a pillow to release tension, headset on table, computer screen with many notifications, dramatic but respectful mood, natural indoor lighting, cinematic, non-stigmatizing, no text'
  },
  {
    file: 'ansiedade.png',
    prompt: 'Photorealistic portrayal of anxiety: an adult repeatedly looking at a wristwatch in a busy urban station, tense posture, worried expression, slight motion blur of crowd around, empathetic tone, natural color grading, non-stigmatizing, no text'
  },
  {
    file: 'burnout.png',
    prompt: 'Photorealistic burnout concept: exhausted office worker late at night in front of laptop, head resting on folded arms, coffee cups and papers around, warm desk lamp and dark surroundings, emotional but respectful, non-stigmatizing, no text'
  },
  {
    file: 'depressao.png',
    prompt: 'Photorealistic, empathetic depression portrait: adult seated by a window with soft overcast light, low energy body language, introspective gaze downward, quiet room, muted tones, respectful and hopeful undertone, no text'
  },
  {
    file: 'panico.png',
    prompt: 'Photorealistic panic episode depiction: adult in crowded public space focusing on breath with hand on chest, blurred surroundings to suggest overwhelm, respectful and calm framing, non-sensational, no text'
  },
  {
    file: 'toc.png',
    prompt: 'Photorealistic OCD representation: adult repeatedly aligning household objects with intense concentration, multiple small corrections visible, clean interior environment, neutral tones, respectful, non-stigmatizing, no text'
  },
  {
    file: 'esquizofrenia.png',
    prompt: 'Photorealistic and compassionate portrayal for schizophrenia: adult in quiet room with reflective expression, subtle abstract sound-wave lighting effects around to suggest auditory hallucinations without caricature, respectful clinical tone, non-stigmatizing, no text'
  }
];

async function generate(){
  for(const p of prompts){
    console.log('Generating', p.file);
    try{
      const res = await fetch('https://api.openai.com/v1/images/generations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${API_KEY}` },
        body: JSON.stringify({ prompt: p.prompt, n:1, size: '1024x1024' })
      });
      if(!res.ok){
        const txt = await res.text();
        console.error('OpenAI API error',res.status, txt);
        continue;
      }
      const data = await res.json();
      // expecting b64_json in data.data[0].b64_json
      const b64 = data.data && data.data[0] && (data.data[0].b64_json || data.data[0].b64);
      if(!b64){ console.error('No image data for', p.file); continue }
      const buf = Buffer.from(b64, 'base64');
      fs.writeFileSync(path.join(outDir, p.file), buf);
      console.log('Saved', p.file);
    }catch(err){
      console.error('Error generating',p.file,err);
    }
  }
}

generate();
