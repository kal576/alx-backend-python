import _asyncio
import aiosqlite

async def async_fetch_users():
    async with aioslite.connect("db_name") as db:
        result = await cursor.fetchall()
        print("All users: ")
        for row in result:
            print(row)
        return result
    
async def async_fetch_older_users():
    async with aioslite.connect("db_name") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            result = await cursor.fetchall()
            for row in result:
                print(row)
            return result

async def fetch_concurrently():
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()

    results = await asyncio.gather(all_users_task, older_users_task)
    all_users, older_users = results

    print("\nSummary:")
    print(f"Total users fetched: {len(all_users)}")
    print(f"Users older than 40: {len(older_users)}")


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())