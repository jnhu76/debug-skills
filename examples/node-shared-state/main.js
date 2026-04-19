function createCustomers(names) {
  const baseSummary = { monthlyTotal: 0, orderCount: 0 };
  const summaries = new Array(names.length).fill(baseSummary);

  return names.map((name, index) => ({
    id: index + 1,
    name,
    summary: summaries[index],
  }));
}

function recordOrder(customer, amount) {
  customer.summary.monthlyTotal += amount;
  customer.summary.orderCount += 1;
}

function main() {
  const customers = createCustomers(["alice", "bob", "carol"]);
  const bob = customers.find((customer) => customer.name === "bob");

  console.log("[before]");
  for (const customer of customers) {
    console.log(customer.name, customer.summary);
  }

  recordOrder(bob, 250);

  console.log("[after recording bob order]");
  for (const customer of customers) {
    console.log(customer.name, customer.summary);
  }

  console.log("Expected: only bob should have monthlyTotal=250 and orderCount=1");
}

main();
