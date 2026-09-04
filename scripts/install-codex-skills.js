#!/usr/bin/env node

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const source = 'Coco131452/coco-skills';
const home = os.homedir();

function commandExists(command) {
  const probe = process.platform === 'win32' ? 'where' : 'which';
  const result = spawnSync(probe, [command], { stdio: 'ignore' });
  return result.status === 0;
}

function detectCodex() {
  if (process.env.CODEX_SESSION_ID || process.env.CODEX_HOME) {
    return true;
  }

  if (commandExists('codex')) {
    return true;
  }

  const candidateDirs = [
    process.env.CODEX_HOME,
    path.join(home, '.codex'),
    path.join(home, '.agents', 'skills'),
  ].filter(Boolean);

  return candidateDirs.some((candidate) => fs.existsSync(candidate));
}

if (!detectCodex()) {
  console.error('未检测到 Codex。请先安装 Codex，或设置 CODEX_HOME 后重试。');
  process.exit(1);
}

const npx = process.platform === 'win32' ? 'npx.cmd' : 'npx';
const result = spawnSync(
  npx,
  [
    '--yes',
    'skills',
    'add',
    source,
    '--skill',
    '*',
    '--agent',
    'codex',
    '-g',
    '-y',
    '--copy',
  ],
  { stdio: 'inherit' },
);

if (result.error) {
  console.error(`执行安装命令失败：${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
