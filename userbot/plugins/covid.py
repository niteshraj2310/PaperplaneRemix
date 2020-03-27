# TG-UserBot - A modular Telegram UserBot script for Python.
# Copyright (C) 2019  Kandarp <https://github.com/kandnub>
#
# TG-UserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TG-UserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TG-UserBot.  If not, see <https://www.gnu.org/licenses/>.

from covid import Covid

from userbot import client
from userbot.utils.events import NewMessage

plugin_category = "pandemic"
covid_str = (
    "**{country}:**  ✅ `{confirmed}` 🦠 `{active}` ⚠️ `{critical}` 💀 `{deaths}` 💚 `{recovered}`"
)


@client.onMessage(command="covid", outgoing=True, regex="covid(?: |$)(.*)")
async def covid19(event: NewMessage.Event) -> None:
    """Get the current covid stats for a specific country or overall."""
    covid = Covid(source="worldometers")
    match = event.matches[0].group(1)
    if match:
        strings = []
        args, _ = await client.parse_arguments(match)
        if match.lower() == "countries":
            strings = sorted(covid.list_countries())
        else:
            for c in args:
                try:
                    country = covid.get_status_by_country_name(c)
                    strings.append(covid_str.format(**country))
                except ValueError:
                    continue
        if strings:
            await event.answer(',\n'.join(strings))
    else:
        country = "Worldwide"
        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()
        string = covid_str.format(country=country,
                                  active=active,
                                  confirmed=confirmed,
                                  recovered=recovered,
                                  deaths=deaths,
                                  critical='?')
        await event.answer(string)
