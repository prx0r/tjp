// Golem xmrig burst — fill POOL/WALLET, set minCpuThreads to provider L3/2MB. Testnet first.
import { GolemNetwork } from "@golem-sdk/golem-js";

const POOL = "pool.example.com:3333";
const WALLET = "YOUR_XMR_ADDRESS";
const order = {
  demand: { workload: { imageTag: "xmrig/xmrig:latest", minCpuThreads: 8 } },
  market: {
    rentHours: 1,
    pricing: { model: "linear", maxStartPrice: 0.5, maxCpuPerHourPrice: 1.0, maxEnvPerHourPrice: 0.5 },
  },
};

const glm = new GolemNetwork({ api: { key: "try_golem" } });
try {
  await glm.connect();
  const exe = await glm.oneOf({ order });
  const res = await exe.run(
    `xmrig -o ${POOL} -u ${WALLET} --tls --huge-pages-jit --donate-level 1`
  );
  console.log(res.stdout);
} finally {
  await glm.disconnect();
}
