import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const dashboardSource = readFileSync(
  new URL("../src/pages/DashboardPage.tsx", import.meta.url),
  "utf8",
);

test("대시보드는 카메라별 stats 를 1초마다 불러 mediamtx path 자가복구를 일으키고, 떠나면 타이머를 정리한다", () => {
  assert.match(
    dashboardSource,
    /for \(const cam of cams\) \{\s*fetch\(`\$\{apiBase\(\)\}\/api\/ipcams\/\$\{cam\.stream_key\}\/stats`\)/,
  );
  assert.match(
    dashboardSource,
    /poll\(\);\s*const id = window\.setInterval\(poll, 1000\);\s*return \(\) => window\.clearInterval\(id\);\s*\}, \[cams\]\);/,
  );
});
